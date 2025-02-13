#!/bin/bash                                                    
#SBATCH --time=0-0:0:5300                                                     
#SBATCH --account=def-vganesh   
#SBATCH --mem=20g         

build=$1
suffix=$2
path=$3
# module load boost
# Get the length of the array
# echo 
i=$(find $path -name "*.cnf" | sed -n "${SLURM_ARRAY_TASK_ID}p")
l=$(wc -l)

if [ ! -f "$i" ] 
then
    echo "Formula $i DOES NOT exist." 
    exit 1
fi

if [ ! -f "$build" ] 
then
    echo "build $build DOES NOT exist." 
    exit 1
fi


filename=$(basename $i)
LOG_FILE="./$path$filename.$suffix.log"
PROOF_FILE="./$path$filename.$suffix.drat"
test -f $LOG_FILE && rm $LOG_FILE
test -f $build && echo $build $suffix
time $build $i $PROOF_FILE &> $LOG_FILE
echo $suffix "${@:4}"
echo run $build $suffix $filename "${@:4}"

