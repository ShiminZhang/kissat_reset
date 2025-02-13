#!/bin/bash                                                    
#SBATCH --time=0-0:0:5300                                                      
#SBATCH --account=def-vganesh   

buildlist=(
    "baseline"
    "partial10"
    "fixed10"
    )
suffixlist=(
    "baseline"
    "partial10"
    "fixed10"
    )
benchmark=(
"./Benchmark_mult/"
)

length=${#buildlist[@]}
benchmark_l=${#benchmark[@]}
timeout_duration=5400

for (( k=0; k<benchmark_l; k++ )); do
    benchmark_path=${benchmark[$k]}
    for (( j=0; j<length; j++ )); do
        build=./build/${buildlist[$j]}
        suffix=${suffixlist[$j]}
        # echo ${test -f $build}
        num_tasks=$(find $benchmark_path -name "*.cnf" | wc -l)
        echo "$build $suffix $benchmark_path $num_tasks"
        for ((t=1; t<num_tasks+1; t++)); do
            file=$(find $benchmark_path -name "*.cnf" | sed -n "${t}p")
            echo "Running: $file"
            timeout "$timeout_duration" $build $file &> ${file}.${suffix}.log
        done
    done
done
