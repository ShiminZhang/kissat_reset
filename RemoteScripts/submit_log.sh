#!/bin/bash                                                    
#SBATCH --time=0-0:0:5300                                                      
#SBATCH --account=def-vganesh   

suffixlist=("llrmab" "tickmab" "kissat" "allstable")
length=${#suffixlist[@]}
benchmark_l=${#benchmark[@]}

module load python/3.10
module load scipy-stack

for (( j=0; j<length; j++ )); do
    suffix=${#suffixlist[$j]}
    sbatch --priority 0 ./RemoteScripts/submit_python_log_single.sh $suffix
done
