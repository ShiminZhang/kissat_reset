#!/bin/bash                                                                    
#SBATCH --time=1-0:0:5300                                                      
#SBATCH --account=def-vganesh                                                  
# SBATCH --mem=10g      

path=../../Benchmark/2024/benchmarks/
# path=../../Benchmark/
# path=./Benchmark_test
build=./build/kissat
suffix=$1
# fixed_p_restart=$2
# interval_flag=$3

# Check if path is an existing directory
if [ ! -d "$path" ] 
then
    echo "Directory $path DOES NOT exist." 
    exit 1
fi

# Check if build is an existing file
if [ ! -f "$build" ]; then
    echo "$build DOES NOT exist."
    exit 1
fi

for i in $(find $path -name "*.cnf"); do 
    # echo $i.$suffix.cadicalreset.log
    # rm $i.$suffix.cadicalreset.log
    filename=$(basename $i)
    test -f $path/kissat/$filename.$suffix.kissatreset.log && rm $path/kissat/$filename.$suffix.kissatreset.log
    sbatch -o $path/kissat/$filename.$suffix.kissatreset.log ./RemoteScripts/submit_kissat_single.sh $build $i $fixed_p_restart $interval_flag ; 
    # ./submit_cadical.sh $build $i $fixed_p_restart $interval_flag > $i.$suffix.cadicalreset.log ; 
done
