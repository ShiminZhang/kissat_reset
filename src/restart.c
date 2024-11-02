#include "restart.h"
#include "backtrack.h"
#include "bump.h"
#include "decide.h"
#include "internal.h"
#include "kimits.h"
#include "logging.h"
#include "print.h"
#include "reluctant.h"
#include "report.h"
#include "inlineheap.h"

#include <inttypes.h>
#include <math.h>
#include <time.h>
#include "Thompson.hpp"
  
#define IntegrateReset false
#define FixedReset true

bool kissat_restarting_reset (kissat *solver) {
  // not implemented
  return false;
}

void randomize_activity_score(kissat *solver){
  // reset scores
  heap* const scores = SCORES;
  for (all_variables (idx)) {
    kissat_update_heap (solver, &solver->scores, idx,(double) rand() / RAND_MAX*0.00001);
  }
  kissat_update_scores(solver);
}

#if MLR
bool kissat_restarting_mlr (kissat *solver) {
  assert(false) // this should not be called now

  if (GET (clauses_learned) > 3 && solver->mlr.conflictsSinceLastRestart > 0) {

      double sigma = sqrt(solver->mlr.m2 / (GET (clauses_learned) - 1));

      double features[7];
      kissat_feature_vector(solver, features);

      double predict = 0;
      for (int i = 0; i < 7; i++) {
          predict += solver->mlr.theta[i] * features[i];
      }

      if (predict > solver->mlr.mu + 3.08 * sigma) {
          solver->mlr.conflictsSinceLastRestart = 0;
          return true;
      }
  }
  return false;
}
#endif

bool kissat_restarting (kissat *solver) {
  assert (solver->unassigned);
  if (!GET_OPTION (restart))
    return false;
  if (!solver->level)
    return false;
  if (CONFLICTS < solver->limits.restart.conflicts)
    return false;
  if (solver->stable)
    return kissat_reluctant_triggered (&solver->reluctant);
  const double fast = AVERAGE (fast_glue);
  const double slow = AVERAGE (slow_glue);
  const double margin = (100.0 + GET_OPTION (restartmargin)) / 100.0;
  const double limit = margin * slow;
  kissat_extremely_verbose (solver,
                            "restart glue limit %g = "
                            "%.02f * %g (slow glue) %c %g (fast glue)",
                            limit, margin, slow,
                            (limit > fast    ? '>'
                             : limit == fast ? '='
                                             : '<'),
                            fast);
  return (limit <= fast);
}

void kissat_update_focused_restart_limit (kissat *solver) {
  assert (!solver->stable);
  limits *limits = &solver->limits;
  uint64_t restarts = solver->statistics.restarts;
  uint64_t delta = GET_OPTION (restartint);
  if (restarts)
    delta += kissat_logn (restarts) - 1;
  limits->restart.conflicts = CONFLICTS + delta;
  kissat_extremely_verbose (solver,
                            "focused restart limit at %" PRIu64
                            " after %" PRIu64 " conflicts ",
                            limits->restart.conflicts, delta);
}

static unsigned reuse_stable_trail (kissat *solver) {
  const heap *const scores = SCORES;
  const unsigned next_idx = kissat_next_decision_variable (solver);
  const double limit = kissat_get_heap_score (scores, next_idx);
  unsigned level = solver->level, res = 0;
  while (res < level) {
    frame *f = &FRAME (res + 1);
    const unsigned idx = IDX (f->decision);
    const double score = kissat_get_heap_score (scores, idx);
    if (score <= limit)
      break;
    res++;
  }
  return res;
}

static unsigned reuse_focused_trail (kissat *solver) {
  const links *const links = solver->links;
  const unsigned next_idx = kissat_next_decision_variable (solver);
  const unsigned limit = links[next_idx].stamp;
  LOG ("next decision variable stamp %u", limit);
  unsigned level = solver->level, res = 0;
  while (res < level) {
    frame *f = &FRAME (res + 1);
    const unsigned idx = IDX (f->decision);
    const unsigned score = links[idx].stamp;
    if (score <= limit)
      break;
    res++;
  }
  return res;
}

static unsigned reuse_trail (kissat *solver) {
  assert (solver->level);
  assert (!EMPTY_STACK (solver->trail));

  if (!GET_OPTION (restartreusetrail))
    return 0;

  unsigned res;

  if (solver->stable)
    res = reuse_stable_trail (solver);
  else
    res = reuse_focused_trail (solver);

  LOG ("matching trail level %u", res);

  if (res) {
    INC (restarts_reused_trails);
    ADD (restarts_reused_levels, res);
    LOG ("restart reuses trail at decision level %u", res);
  } else
    LOG ("restarts does not reuse the trail");

  return res;
}

#if MAB
void restart_mab(kissat * solver){   
	unsigned stable_restarts = 0;
	solver->mab_reward[solver->heuristic] += !solver->mab_chosen_tot?0:log2(solver->mab_decisions)/solver->mab_chosen_tot;
	for (all_variables (idx)) solver->mab_chosen[idx]=0;
	solver->mab_chosen_tot = 0;
	solver->mab_decisions = 0;
	for(unsigned i=0;i<solver->mab_heuristics;i++) stable_restarts +=  solver->mab_select[i];
	if(stable_restarts < solver->mab_heuristics) {
		solver->heuristic = solver->heuristic==0?1:0; 
	}else{
		double ucb[2];
		solver->heuristic = 0;
		for(unsigned i=0;i<solver->mab_heuristics;i++) {
		     ucb[i] = solver->mab_reward[i]/solver->mab_select[i] + sqrt(solver->mabc*log(stable_restarts+1)/solver->mab_select[i]);
		     if(i!=0 && ucb[i]>ucb[solver->heuristic]) solver->heuristic = i;
		  }
	}
	solver->mab_select[solver->heuristic]++; 
}


void kissat_restart_mab(kissat *solver) {
  unsigned old_heuristic = solver->heuristic;
  if (solver->stable && solver->mab) 
     restart_mab(solver);
  unsigned new_heuristic = solver->heuristic;

  unsigned level = old_heuristic==new_heuristic?reuse_trail (solver):0;

  
  if (solver->stable && solver->mab) solver->heuristic = old_heuristic;
  kissat_backtrack_in_consistent_state (solver, level);
  if (solver->stable && solver->mab) solver->heuristic = new_heuristic;
if(level != 0){
    //printf("decisions: %d\n", solver->reset_decisions);
    //printf("conflicts: %d\n", solver->reset_conflicts);
    // Seed the random number generator
    srand(time(NULL));

    //Thompson

    //compute local learning rate
    double localLearningRate = (solver->reset_conflicts * 1.0) / solver->reset_decisions;
    solver-> reset_conflicts = 0;
    solver-> reset_decisions = 0;
    //printf("local learning rate: %0.2f\n", localLearningRate);
    //printf("learning rateEMB: %0.2f\n\n", solver->learningRateEMA);
    //update success and failures
    if (solver-> resetTotalTimes != 0){
      if (localLearningRate >= solver->learningRateEMA){
        	if (solver->resetPrevLever == 0){
        	  solver->reset_wins++;
        	}
        	else{
        	  solver->restart_wins++;
        	}
      }
      else{
      	if (solver->resetPrevLever == 0){
      	  solver->reset_loses++;
      	}
      	else{
      	  solver->restart_loses++;
      	}
      }
    }
    //update LLR-MAB
    solver-> learningRateEMA *= solver-> resetDecay;
    solver->learningRateEMA += localLearningRate * (1.0 - solver->resetDecay);

    // printf("reset_wins: %0.2f\n", solver->reset_wins);
    // printf("reset_loses: %0.2f\n", solver->reset_loses);
    // printf("restart_wins: %0.2f\n", solver->restart_wins);
    // printf("restart_loses: %0.2f\n", solver->restart_loses);
    //select a lever
    solver->resetPrevLever = select_lever(solver->reset_wins, solver->reset_loses, solver->restart_wins, solver->restart_loses);
    solver->resetTotalTimes++;
    if (solver->resetPrevLever == 0){
      solver->reset_wins *= solver->resetDecay;
      solver->reset_loses *= solver->resetDecay;
    }
    else{
      solver->restart_wins *= solver->resetDecay;
      solver->restart_loses *= solver->resetDecay;
    }

    //printf("lever: %d\n\n",solver->resetPrevLever);

    // Probability of the event occurring (e.g. 0.3 means 30% chance)
    //double probability = 0.5;
    // Generate a random number between 0 and 1
    //double random_number = (double) rand() / RAND_MAX;
    // Check if the event occurs
    //if (random_number <= probability) {
    if (solver->resetPrevLever == 0) {
      // Event occurred, execute the code here
      //reset activities
      for (all_variables(idx)) {
        kissat_update_heap(solver, &solver->scores, idx, (double) rand() / RAND_MAX*0.00001);
      }
      //update scores
      heap *scores = SCORES;
      for (all_variables (idx))
        if (ACTIVE (idx) && !kissat_heap_contains (scores, idx))
          kissat_push_heap (solver, scores, idx);
      solver->nof_resets++;
    }
    else{
      solver->nof_restarts++; 
    }
  }
  else{
    solver->nof_restarts++;  
  }

  
  if (!solver->stable)
    kissat_update_focused_restart_limit (solver);
  if (solver->stable && solver->mab && old_heuristic!=new_heuristic) kissat_update_scores(solver);
}
#endif

void kissat_restart (kissat *solver) {
  START (restart);
  INC (restarts);

#if MAB
  assert(false) // this should not be called for now

  // simply forward there
  kissat_restart_mab(solver);
  
  REPORT (1, 'R');
  STOP (restart); 
  return
#endif

  ADD (restarts_levels, solver->level);
  if (solver->stable){
    INC (stable_restarts);
    // printf ("mylog: stable restart");
  } else {
    INC (focused_restarts);
    // printf ("mylog: focused restart");
  }
  unsigned level = reuse_trail (solver);
  kissat_extremely_verbose (solver,
                            "restarting after %" PRIu64 " conflicts"
                            " (limit %" PRIu64 ")",
                            CONFLICTS, solver->limits.restart.conflicts);
  LOG ("restarting to level %u", level);
  // printf ("mylog: restart to %u \n", level);
  kissat_backtrack_in_consistent_state (solver, level);

#if FixedReset
    srand(time(NULL));
    //Probability of the event occurring (e.g. 0.3 means 30% chance)
    double probability = 0.05;
    //Generate a random number between 0 and 1
    double random_number = (double) rand() / RAND_MAX;
    if (random_number <= probability) {
      randomize_activity_score(solver);
    }
#endif
  if (!solver->stable){
#if IntegrateReset
    randomize_activity_score(solver);
#endif
    kissat_update_focused_restart_limit (solver);
  }

  REPORT (1, 'R');
  STOP (restart);
}


// what's the difference between reset and others
void kissat_reset (kissat *solver){
  unsigned level = reuse_trail (solver);
  kissat_backtrack_in_consistent_state (solver, level);
  if (!solver->stable)
    kissat_update_focused_restart_limit (solver);

  randomize_activity_score(solver);
}