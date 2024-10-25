#!/bin/bash                                                                    
#SBATCH --time=0-0:0:5300 
#SBATCH --account=def-vganesh                                                  
#SBATCH --mem=10g                                                               

build=$1
# fixed_p_reset=$3
file=$2
# flag=--fixed-p-reset
# if [ -z "$4" ] 
# then
#     flag=--fixed-p-reset
# else
#     flag=--fixed-interval-reset
# fi

# time $build $flag $fixed_p_reset $file
time $build $file