#!/bin/bash                                                    
#SBATCH --time=0-0:0:5300                                                      
#SBATCH --account=def-vganesh   

suffixlist=("cnf.200" "cnf.300" "cnf.400" "cnf.500" "cnf.600" "cnf.700" "cnf.800" "cnf.900")
length=${#suffixlist[@]}

for (( j=0; j<length; j++ )); do
    suffix=${suffixlist[$j]}
    echo $j $suffix
    sbatch -o ./Outputs/log_single_process$suffix.log --priority 0 ./RemoteScripts/submit_python_log_single.sh $suffix
done
