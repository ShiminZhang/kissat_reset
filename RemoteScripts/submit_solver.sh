#!/bin/bash                                                                    
#SBATCH --time=1-0:0:5300                                                      
#SBATCH --account=def-vganesh                                                  
# SBATCH --mem=10g      

path=../Benchmark/2023/benchmarks/
# path=../../Benchmark/sbva/
# path=./Benchmark_test/

buildlist=("baseline" "fixed05" "fixed05" "fixed05" "fixed05" "fixed05" "fixed05" "fixed05" "fixed05" "fixed05")
# buildlist=("cadical_original" "cadical_f05")
suffixlist=("baseline" "f05a" "f05b" "f05c" "f05d" "f05e" "f05f" "f05g" "f05h" "f05i")
# suffixlist=("2023champion" "2023with05")

# build=$1
# fixed_p_restart=$2
# interval_flag=$3

# Check if path is an existing directory
if [ ! -d "$path" ] 
then
    echo "Directory $path DOES NOT exist." 
    exit 1
fi

# Get the length of the array
length=${#buildlist[@]}

for i in $(find $path -name "*.cnf"); do 
# for i in $(find $path -name "*.sbva"); do 
    filename=$(basename $i)
    # for (( j=0; j<length; j++ )); do
    for (( j=0; j<length; j++ )); do
        # build=./build/${buildlist[j]}
        build=./build/fixed05
        # suffix=${suffixlist[j]}
        suffix=f05duplicate$j
        test -f $build && echo $build $suffix
        test -f $path/kissat/$filename.$suffix.kissatreset.log && rm $path/kissat/$filename.$suffix.kissatreset.log
        sbatch -o $path/kissat/$filename.$suffix.kissatreset.log ./RemoteScripts/submit_kissat_single.sh $build $i $fixed_p_restart $interval_flag ;
    done
    # ./submit_cadical.sh $build $i $fixed_p_restart $interval_flag > $i.$suffix.cadicalreset.log ; 
done
