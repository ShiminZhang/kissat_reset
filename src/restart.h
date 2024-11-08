#ifndef _restart_h_INCLUDED
#define _restart_h_INCLUDED

#include <stdbool.h>

struct kissat;

bool kissat_restarting (struct kissat *);
bool kissat_restarting_mlr (struct kissat *);
bool kissat_restarting_reset (struct kissat *);

void kissat_restart (struct kissat *);
void kissat_reset (struct kissat *);
// void reset (struct kissat *);

void kissat_update_focused_restart_limit (struct kissat *);

#endif
