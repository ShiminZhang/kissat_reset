#!/bin/bash                                                    
#SBATCH --time=0-0:0:5300                                                      
#SBATCH --account=def-vganesh   

# buildlist=("cadical-uip" "cadical-dip" "kissat")
# suffixlist=("cadical-uip" "cadical-dip" "kissat")
# buildlist=("llrmab" "tickmab" "kissat" "allstable" "allfocus")
# suffixlist=("llr" "tick" "kissat" "allstable" "allfocus")
buildlist=("tickfix")
suffixlist=("tickfix")
benchmark=("./Benchmark/2023/benchmarks/")
# benchmark=("./kissat_reset/Benchmark_test")
# ERCLbench="./ERCL/dip-paper-benchs/"
# benchmark=("./ERCL/dip-paper-benchs/randkxor/")
# benchmark=("./$ERCLbench/intervals/" "./$ERCLbench/tseitin-4-regular/" "./$ERCLbench/tseitin-6-regular/" "./$ERCLbench/tseitin-grid/")
# benchmark=("./$ERCLbench/intervals/")
# Get the length of the array
length=${#buildlist[@]}
benchmark_l=${#benchmark[@]}

for (( k=0; k<benchmark_l; k++ )); do
    benchmark_path=${benchmark[$k]}
    for (( j=0; j<length; j++ )); do
        build=./kissat_reset/build/${buildlist[$j]}
        suffix=${suffixlist[$j]}
        # echo ${test -f $build}
        num_tasks=$(find $benchmark_path -name "*.cnf" | wc -l)
        echo "$build $suffix $benchmark_path $num_tasks"
        # sbatch --array=1-500 ./array_submit_solver.sh $build $suffix $benchmark_path
        for (( jj=0; jj<10000;)); do
            jj=$((jj+1000))
            # sbatch --priority 1 -o ./output/output_%A_%a.out --array=1-${num_tasks} ./array_submit_solver.sh $build $suffix $benchmark_path
            jobid=$(sbatch --priority 1 -o ./output/output_%A_%a_$jj.out --array=1-${num_tasks} ./array_submit_solver.sh $build ${suffix}_${jj} $benchmark_path "--tick_limit_reset" $jj | awk '{print $4}')
            echo "Submitted job with ID: $jobid" ${suffix}_${jj}
            sbatch --dependency=afterok:$jobid -o ./Outputs/log_single_process/$suffix.log --priority 0 ./RemoteScripts/submit_python_log_single.sh $suffix
        done
    done
done
