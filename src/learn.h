#ifndef _learn_h_INCLUDED
#define _learn_h_INCLUDED

struct kissat;

void kissat_learn_clause (struct kissat *);
void kissat_update_learned (struct kissat *, unsigned glue, unsigned size);
unsigned kissat_determine_new_level (struct kissat *, unsigned jump);
void kissat_feature_vector (struct kissat *solver, double *features);

#endif
