#!/bin/bash                                                    
#SBATCH --time=0-0:0:5300                                                      
#SBATCH --account=def-vganesh   

# buildlist=("cadical-uip" "cadical-dip" "kissat")
# suffixlist=("cadical-uip" "cadical-dip" "kissat")
# buildlist=("llrmab" "tickmab" "kissat" "allstable" "allfocus")
# suffixlist=("llr" "tick" "kissat" "allstable" "allfocus")
# buildlist=("tickEMA")
# suffixlist=("tickEMA")
buildlist=("tickbase")
suffixlist=("tickbase")
benchmark=("../Benchmark/2024/benchmarks/")
# benchmark=("./Benchmark_test")
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
        build=./build/${buildlist[$j]}
        suffix=${suffixlist[$j]}
        # echo ${test -f $build}
        num_tasks=$(find $benchmark_path -name "*.cnf" | wc -l)
        echo "$build $suffix $benchmark_path $num_tasks"
        # sbatch --array=1-500 ./array_submit_solver.sh $build $suffix $benchmark_path
        # for (( jj=100; jj<500;)); do
        # for (( jj=30; jj<100;)); do
            # sbatch --priority 1 -o ./output/output_%A_%a.out --array=1-${num_tasks} ./array_submit_solver.sh $build $suffix $benchmark_path
            # jobid=$(sbatch --priority 1 -o ./Outputs/output_%A_%a_$jj.out --array=1-${num_tasks} ./RemoteScripts/array_submit_solver.sh $build ${suffix}_${jj} $benchmark_path "--tick_limit_reset" $jj | awk '{print $4}')
            # echo "Submitted job with ID: $jobid" ${suffix}_${jj}
            # sleep 1s
            # sbatch --dependency=afterok:$jobid -o ./Outputs/log_single_process/$suffix.log --priority 0 ./RemoteScripts/submit_python_log_single.sh $suffix
            # jj=$((jj+100))
        # done

        jobid=$(sbatch --priority 1 -o ./Outputs/output_%A_%a.out --array=1-${num_tasks} ./RemoteScripts/array_submit_solver.sh $build ${suffix} $benchmark_path | awk '{print $4}')
        echo "Submitted job with ID: $jobid" ${suffix}
        sleep 1s
        sbatch --dependency=afterok:$jobid -o ./Outputs/log_single_process/$suffix.log --priority 0 ./RemoteScripts/submit_python_log_single.sh $suffix
    done
done
