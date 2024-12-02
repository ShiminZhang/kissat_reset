#!/bin/bash                                                    
#SBATCH --time=0-0:0:5300                                                      
#SBATCH --account=def-vganesh   


module load python/3.10
module load scipy-stack

python ./RemoteScripts/draw_cactus.py $suffix
