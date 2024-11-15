#!/bin/bash                                                    
#SBATCH --time=0-0:0:5300                                                      
#SBATCH --account=def-vganesh   

buildlist=("kissat_mab" "allstable" "allfocus" "vanilla")
suffixlist=("mab" "allstable" "allfocus" "baseline")
# benchmark=("./Benchmark_test/")
benchmark=("../Benchmark/2024/benchmarks/")
# buildlist=("baseline" "fixed05" "fixed05" "fixed05" "fixed05" "fixed05" "fixed05" "fixed05" "fixed05" "fixed05")
# suffixlist=("baseline" "f05a" "f05b" "f05c" "f05d" "f05e" "f05f" "f05g" "f05h" "f05i")
# buildlist=("kissat_fixseed" "kissat_fixseed" "kissat_fixseed" "kissat_fixseed" "kissat_fixseed" "kissat_fixseed" "kissat_fixseed" "kissat_fixseed" "kissat_fixseed")
# suffixlist=("fixseeda" "fixseedb" "fixseedc" "fixseedd" "fixseede" "fixseedf" "fixseedg" "fixseedh" "fixseedi")

# Get the length of the array
length=${#buildlist[@]}
benchmark_l=${#benchmark[@]}
echo $length $benchmark_l
for (( k=0; k<benchmark_l; k++ )); do
    benchmark_path=${benchmark[$k]}
    for (( j=0; j<length; j++ )); do
        build=./build/${buildlist[$j]}
        suffix=${suffixlist[$j]}
        # echo ${test -f $build}
        num_tasks=$(find $benchmark_path -name "*.cnf" | wc -l)
        echo "$build $suffix $benchmark_path $num_tasks"
        sbatch -o $benchmark_path$suffix.$build._%A_%a.log --array=1-${num_tasks} ./RemoteScripts/array_submit_solver.sh $build $suffix $benchmark_path
    done
done
