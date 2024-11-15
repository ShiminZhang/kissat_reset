#!/bin/bash                                                    
#SBATCH --time=0-0:0:5300                                                      
#SBATCH --account=def-vganesh   

suffix=$1

module load python/3.10
module load scipy-stack

python ./RemoteScripts/process_log_single.py $suffix
