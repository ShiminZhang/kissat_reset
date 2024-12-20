#include "bump.h"
#include "decide.h"
#include "inline.h"
#include "print.h"
#include "report.h"
#include "resources.h"
#include "restart.h"

#include <inttypes.h>

#ifndef QUIET

static const char *mode_string (kissat *solver) {
  return solver->stable ? "stable" : "focused";
}

#endif

void kissat_init_mode_limit (kissat *solver) {
  limits *limits = &solver->limits;

  if (GET_OPTION (stable) == 1) {
    assert (!solver->stable);

    const uint64_t conflicts_delta = GET_OPTION (modeinit);
    const uint64_t conflicts_limit = CONFLICTS + conflicts_delta;

    assert (conflicts_limit);

    limits->mode.conflicts = conflicts_limit;
    limits->mode.ticks = 0;
    limits->mode.count = 0;

    kissat_very_verbose (solver,
                         "initial %s mode switching limit "
                         "at %s after %s conflicts",
                         mode_string (solver),
                         FORMAT_COUNT (conflicts_limit),
                         FORMAT_COUNT (conflicts_delta));

    solver->mode.ticks = solver->statistics.search_ticks;
#ifndef QUIET
    solver->mode.conflicts = CONFLICTS;
#ifdef METRICS
    solver->mode.propagations = solver->statistics.search_propagations;
#endif
    // clang-format off
      solver->mode.entered = kissat_process_time ();
      kissat_very_verbose (solver,
        "starting %s mode at %.2f seconds "
        "(%" PRIu64 " conflicts, %" PRIu64 " ticks"
#ifdef METRICS
	", %" PRIu64 " propagations, %" PRIu64 " visits"
#endif
	")", mode_string (solver),
        solver->mode.entered, solver->mode.conflicts, solver->mode.ticks
#ifdef METRICS
        , solver->mode.propagations, solver->mode.visits
#endif
	);
// clang-format on
#endif
  } else
    kissat_very_verbose (solver,
                         "no need to set mode limit (only %s mode enabled)",
                         mode_string (solver));
}

static void update_mode_limit (kissat *solver, uint64_t delta_ticks) {
  kissat_init_averages (solver, &AVERAGES);

  limits *limits = &solver->limits;
  statistics *statistics = &solver->statistics;

  assert (GET_OPTION (stable) == 1);

  if (limits->mode.count & 1) {
    limits->mode.ticks = statistics->search_ticks + delta_ticks;
#ifndef QUIET
    assert (solver->stable);
    kissat_phase (solver, "stable", GET (stable_modes),
                  "new stable mode switching limit of %s "
                  "after %s ticks",
                  FORMAT_COUNT (limits->mode.ticks),
                  FORMAT_COUNT (delta_ticks));
#endif
  } else {
    assert (limits->mode.ticks);
    const uint64_t interval = GET_OPTION (modeint); //1e3
    const uint64_t count = (statistics->switched + 1) / 2; // increased on every switch
    const uint64_t scaled = interval * kissat_nlogpown (count, 4);//count*(log_10(count+9))^4
    limits->mode.conflicts = statistics->conflicts + scaled;
#ifndef QUIET
    assert (!solver->stable);
    kissat_phase (solver, "focused", GET (focused_modes),
                  "new focused mode switching limit of %s "
                  "after %s conflicts",
                  FORMAT_COUNT (limits->mode.conflicts),
                  FORMAT_COUNT (scaled));
#endif
  }

  solver->mode.ticks = statistics->search_ticks;
#ifndef QUIET
  solver->mode.conflicts = statistics->conflicts;
#ifdef METRICS
  solver->mode.propagations = statistics->search_propagations;
#endif
#endif
}

static void report_switching_from_mode (kissat *solver,
                                        uint64_t *delta_ticks) {
  statistics *statistics = &solver->statistics;
  *delta_ticks = statistics->search_ticks - solver->mode.ticks;

#ifndef QUIET
  if (kissat_verbosity (solver) < 2)
    return;

  const double current_time = kissat_process_time ();
  const double delta_time = current_time - solver->mode.entered;

  const uint64_t delta_conflicts =
      statistics->conflicts - solver->mode.conflicts;
#ifdef METRICS
  const uint64_t delta_propagations =
      statistics->search_propagations - solver->mode.propagations;
#endif
  solver->mode.entered = current_time;

  // clang-format off
  kissat_very_verbose (solver, "%s mode took %.2f seconds "
    "(%s conflicts, %s ticks"
#ifdef METRICS
    ", %s propagations"
#endif
    ")", solver->stable ? "stable" : "focused",
    delta_time, FORMAT_COUNT (delta_conflicts), FORMAT_COUNT (*delta_ticks)
#ifdef METRICS
    , FORMAT_COUNT (delta_propagations)
#endif
    );
  // clang-format on
#else
  (void) solver;
#endif
}

static void switch_to_focused_mode (kissat *solver) {
  assert (solver->stable);
  uint64_t delta;
  report_switching_from_mode (solver, &delta);
  REPORT (0, ']');
  STOP (stable);
  INC (focused_modes);
  kissat_phase (solver, "focus", GET (focused_modes),
                "switching to focused mode after %s conflicts",
                FORMAT_COUNT (CONFLICTS));
  solver->stable = false;
  update_mode_limit (solver, delta);
  START (focused);
  REPORT (0, '{');
  kissat_reset_search_of_queue (solver);
  kissat_update_focused_restart_limit (solver);
}

static void switch_to_stable_mode (kissat *solver) {
  assert (!solver->stable);
  uint64_t delta;
  report_switching_from_mode (solver, &delta);
  REPORT (0, '}');
  STOP (focused);
  INC (stable_modes);
  solver->stable = true;
  kissat_phase (solver, "stable", GET (stable_modes),
                "switched to stable mode after %" PRIu64 " conflicts",
                CONFLICTS);
  update_mode_limit (solver, delta);
  START (stable);
  REPORT (0, '[');
  kissat_init_reluctant (solver);
  kissat_update_scores (solver);
}
#if RL
bool RL_switching_search_mode(kissat *solver) {
  if (solver->rl_decisions == 0) return false;

  double localLearningRate = (solver->rl_conflicts * 1.0) / solver->rl_decisions;
  solver->rl_conflicts = 0;
  solver->rl_decisions = 0;

  int choice_stable = 0;
  int choice_focus = 1;
  int choice_explore = 2;

  if (localLearningRate > solver->EMALR) {
    if (solver->chosen_arm == choice_stable) {
      solver->stable_wins++;
    } else if (solver->chosen_arm == choice_focus) {
      solver->focus_wins++;
    } else if (solver->chosen_arm == choice_explore) {
      solver->aggressive_wins++;
    }
  } else {
    if (solver->chosen_arm == choice_stable) {
      solver->stable_loses++;
    } else if (solver->chosen_arm == choice_focus) {
      solver->focus_loses++;
    } else if (solver->chosen_arm == choice_explore) {
      solver->aggressive_loses++;
    }
  }

  solver->EMALR *= 0.8;
  solver->EMALR += localLearningRate * (1.0 - 0.8);

  solver->chosen_arm = select_lever(
    solver->stable_wins, solver->stable_loses,
    solver->focus_wins, solver->focus_loses,
    solver->aggressive_wins, solver->aggressive_loses
  );

  solver->nof_deciding++;
  if (solver->chosen_arm == choice_stable) {
    solver->stable_wins *= 0.8;
    solver->stable_loses *= 0.8;
    solver->nof_stable++;
  } else if (solver->chosen_arm == choice_focus) {
    solver->focus_wins *= 0.8;
    solver->focus_loses *= 0.8;
    solver->nof_focus++;
  } else if (solver->chosen_arm == choice_explore) {
    solver->aggressive_wins *= 0.8;
    solver->aggressive_loses *= 0.8;
    solver->nof_aggresive++;
  }

  bool should_stable = (solver->chosen_arm == choice_stable);
  if (should_stable == solver->stable) {
    return false;
  } else {
    return true;
  }
}
#endif

bool kissat_switching_search_mode (kissat *solver) {
  assert (!solver->inconsistent);

  if (GET_OPTION (stable) != 1)
    return false;

  limits *limits = &solver->limits;
  statistics *statistics = &solver->statistics;
  if (limits->mode.count & 1) //wuts this count?
#if RL
    if (statistics->search_ticks >= limits->mode.ticks){
      return RL_switching_search_mode(solver);
    }
#else
    return statistics->search_ticks >= limits->mode.ticks;
#endif
  else
    return statistics->conflicts >= limits->mode.conflicts;
}

void kissat_switch_search_mode (kissat *solver) {
#if RL
#else
  assert (kissat_switching_search_mode (solver));
#endif

  INC (switched);
  solver->limits.mode.count++;

  if (solver->stable)
    switch_to_focused_mode (solver);
  else
    switch_to_stable_mode (solver);

  solver->averages[solver->stable].saved_decisions = DECISIONS;

  kissat_start_random_sequence (solver);
}
