#include "mlr.h"
#include "internal.h"

#if MLR
void kissat_init_mlr (struct kissat * solver) {
    solver->mlr.prevLbd1 = 0;
    solver->mlr.prevLbd2 = 0;
    solver->mlr.prevLbd3 = 0;
    solver->mlr.mu = 0;
    solver->mlr.m2 = 0;
    solver->mlr.conflictsSinceLastRestart = 0;
    solver->mlr.t = 0;


    // Initialize Adam parameters (e.g., theta, m, v)
    for (int i = 0; i < 5; i++) {
        solver->mlr.theta[i] = 0;
        solver->mlr.m[i] = 0;
        solver->mlr.v[i] = 0;
    }
}
#endif