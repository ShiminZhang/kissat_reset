#!/bin/bash                            
#SBATCH --time=0-0:0:30000                                                      
#SBATCH --account=def-vganesh   
#SBATCH --mem=20g         


module load python/3.10
# module load scipy-stack
# source ../venv/bin/activate

input_cnf=$1
input_proof=$2
input_log=$3
dir=$(dirname $input_cnf)
base=$(basename $input_cnf)

drat="../libs/drat-trim"
echo $1 $2 $3
# $drat $input_cnf $input_proof -l ${input_cnf}.lemmas
# python ./RemoteScripts/calculateLBD.py ${input_cnf}.lemmas $input_log > ${input_cnf}.stat