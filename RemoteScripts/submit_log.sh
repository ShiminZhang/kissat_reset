#!/bin/bash                                                    
#SBATCH --time=0-0:0:5300                                                      
#SBATCH --account=def-vganesh   

# suffixlist=("tickEMA_30" "tickEMA_40" "tickEMA_50" "tickEMA_60" "tickEMA_70" "tickEMA_80" "tickEMA_90")
suffixlist=("fixed10" "fixed15" "fixed05" "baseline")
length=${#suffixlist[@]}

for (( j=0; j<length; j++ )); do
    suffix=${suffixlist[$j]}
    echo $j $suffix
    sbatch -o ./Outputs/log_single_process$suffix.log --priority 0 ./RemoteScripts/submit_python_log_single.sh $suffix
done
