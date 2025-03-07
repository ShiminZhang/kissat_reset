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
#define FixedReset true
#define PartialResetK 25
#include <stdio.h>

typedef struct {
  double value;
  int index;
} element_t;
// Swap function
void swap(element_t *a, element_t *b) {
  element_t temp = *a;
  *a = *b;
  *b = temp;
}

// Max-Heapify function
void max_heapify(element_t heap[], int size, int i) {
  int largest = i;
  int left = 2 * i + 1;
  int right = 2 * i + 2;

  if (left < size && heap[left].value > heap[largest].value)
      largest = left;
  
  if (right < size && heap[right].value > heap[largest].value)
      largest = right;
  
  if (largest != i) {
      swap(&heap[i], &heap[largest]);
      max_heapify(heap, size, largest);
  }
}

// Extract max (root) from the heap
element_t extract_max(element_t heap[], int *size) {
  if (*size <= 0) return (element_t){-1, -1};

  element_t max_element = heap[0];

  // Move the last element to root and reduce heap size
  heap[0] = heap[*size - 1];
  (*size)--;

  // Restore heap property
  max_heapify(heap, *size, 0);

  return max_element;
}

// Function to get top K elements and their positions without modifying arr
void find_top_k(heap* inHeap, unsigned n, unsigned k, double top_k_scores[], unsigned top_k_indices[]) {
  if (k <= 0 || k > n) {
      // printf("Invalid value of K\n");
      return;
  }

  // Create a copy of the heap with original indices
  element_t heap[n];
  for (unsigned i = 0; i < n; i++) {
      unsigned lit = PEEK_STACK (inHeap->stack, i);
      double score = kissat_get_heap_score (inHeap, lit);
      heap[i].value = score;
      heap[i].index = i;
  }

  int heap_size = n;

  for (unsigned i = 0; i < k; i++) {
      element_t max_element = extract_max(heap, &heap_size);
      top_k_scores[i] = max_element.value;
      top_k_indices[i] = max_element.index;
  }
}

void randomize_activity_score(kissat *solver){
#ifdef PartialResetK
  heap *heap = &solver->scores;
  unsigned valid_K = MIN(PartialResetK, solver->vars);
  // unsigned valid_K = MIN(kissat_size_heap(heap), solver->vars);
  unsigned K_lits[valid_K];
  unsigned K_pos[valid_K];
  double K_scores[valid_K];
  double max_score_in_K = 0;
  double max_score_in_random = 0;

  if (kissat_empty_heap (heap))
    return;

  find_top_k(heap, kissat_size_heap(heap), valid_K, K_scores, K_pos);

  for (unsigned rank = 0; rank < valid_K; rank++){
      unsigned pos = K_pos[rank];
      K_lits[rank] = PEEK_STACK(heap->stack, pos);;
  }
#endif

  for (unsigned idx = 0; idx < solver->vars; idx++ ) {
    double new_score = (double) rand() / RAND_MAX * 0.00001;
#ifdef PartialResetK
    max_score_in_random = max_score_in_random > new_score ? max_score_in_random : new_score;
#endif
    kissat_update_heap (solver, &solver->scores, idx, new_score);
  }

  #ifdef PartialResetK
    max_score_in_K = K_scores[0];
    for (unsigned i = 0; i < valid_K; i++){
      unsigned lit = K_lits[i];
      // assert(K_scores[i] > 0);
      if (K_scores[i] < 0){
        break;
      }
      double new_score = max_score_in_random + K_scores[i] / max_score_in_K;
      kissat_update_heap (solver, &solver->scores, lit, new_score);
    }
  #endif

  kissat_update_scores(solver);
}

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

void kissat_restart (kissat *solver) {
  START (restart);
  INC (restarts);
  ADD (restarts_levels, solver->level);
  if (solver->stable)
    INC (stable_restarts);
  else
    INC (focused_restarts);
  unsigned level = reuse_trail (solver);
  kissat_extremely_verbose (solver,
                            "restarting after %" PRIu64 " conflicts"
                            " (limit %" PRIu64 ")",
                            CONFLICTS, solver->limits.restart.conflicts);
  LOG ("restarting to level %u", level);
  kissat_backtrack_in_consistent_state (solver, level);
  if (!solver->stable){
#if FixedReset
      double probability = 0.05;
      double random_number = (double) rand() / RAND_MAX;
      if (random_number <= probability) {
        randomize_activity_score(solver);
      }
#endif
    kissat_update_focused_restart_limit (solver);
  }
  REPORT (1, 'R');
  STOP (restart);
}
