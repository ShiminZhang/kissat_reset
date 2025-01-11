#!/bin/bash

jobids=$(squeue -u $USER -h -o "%i")
sbatch --dependency=afterok:$jobids get_all_stat.sh
