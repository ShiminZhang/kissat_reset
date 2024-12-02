#!/bin/bash                                                    
#SBATCH --time=0-0:0:5300                                                      
#SBATCH --account=def-vganesh   

# suffixlist=("tickEMA_30" "tickEMA_40" "tickEMA_50" "tickEMA_60" "tickEMA_70" "tickEMA_80" "tickEMA_90")
suffixlist=("tickfix_100" "tickfix_200" "tickfix_300" "tickfix_400")
length=${#suffixlist[@]}

for (( j=0; j<length; j++ )); do
    suffix=${suffixlist[$j]}
    echo $j $suffix
    sbatch -o ./Outputs/log_single_process$suffix.log --priority 0 ./RemoteScripts/submit_python_log_single.sh $suffix
done
