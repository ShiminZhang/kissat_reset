#!/bin/bash                                                    
#SBATCH --time=0-0:0:5300                                                      
#SBATCH --account=def-vganesh   

# buildlist=("cadical-uip" "cadical-dip" "kissat")
# suffixlist=("cadical-uip" "cadical-dip" "kissat")
# buildlist=("llrmab" "tickmab" "kissat" "allstable" "allfocus")
# suffixlist=("llr" "tick" "kissat" "allstable" "allfocus")
# buildlist=("tickEMA")
# suffixlist=("tickEMA")
# buildlist=("baseline")
# suffixlist=("baseline")
# buildlist=("fixed05")
# suffixlist=("fixed05")
# buildlist=("tickfix")
# suffixlist=("tickfix")
# buildlist=("fixed40" "fixed50")
# suffixlist=("fixed40" "fixed50")
# buildlist=("fixed15" "fixed20" "fixed30" "baseline" "fixed13" "fixed10"  "fixed05" "fixed07" "fixed40" "fixed50" "fixed10" "fixed10" "fixed10" "fixed10" "fixed10" "fixed10" "fixed10" "fixed10" "fixed10" "fixed10") 
# suffixlist=("fixed15" "fixed20" "fixed30" "baseline" "fixed13" "fixed10" "fixed05" "fixed07" "fixed40" "fixed50" "f10a" "f10b" "f10c" "f10d" "f10e" "f10f" "f10g" "f10h" "f10i" "f10j")
# buildlist=("fixed05" "fixed20" "baseline" "fixed15" "fixed10")
# suffixlist=("fixed05" "fixed20" "baseline" "fixed15" "fixed10")

buildlist=(
    "reset05decay10"
    "baselinedecay10"
    # # "reset05decay20"
    # "reset05decay30"
    # # "reset05decay40"
    "baselinedecay40"
    # # "reset05decay50"

    # # "reset05decay60"
    # # "reset05decay70"
    # # "reset05decay80"
    "baselinedecay60"
    "baselinedecay70"
    "baselinedecay80"
    # "reset05decay90"
    # "baselinedecay90"
    )
suffixlist=(
    "reset05decay10"
    "baselinedecay10"
    # # "reset05decay20"
    # "reset05decay30"
    # # "reset05decay40"
    "baselinedecay40"
    # # "reset05decay50"

    # # "reset05decay60"
    # # "reset05decay70"
    # # "reset05decay80"
    "baselinedecay60"
    "baselinedecay70"
    "baselinedecay80"
    # "reset05decay90"
    # "baselinedecay90"
    )
# buildlist=(
#     # "fixed05"
#     # "baseline"
#     # "baseline_nocongruence"
#     # "fixed05_nocongruence"
#     # "fixed05_stat"
#     # "fixed10_stat"
#     # "baseline_stat"
#     # "fixed05_stattest"
#     "stattest"
#     "dumptest"
#     "stattest"
#     "dumptest"
#     # "partial5"
#     )

# suffixlist=(
#     # "fixed05"
#     # "baseline"
#     # "baseline_nocongruence"
#     # "fixed05_nocongruence"
#     # "fixed05_stat"
#     # "fixed10_stat"
#     "stattest1"
#     "dumptest1"
#     "stattest2"
#     "dumptest2"
#     # "baseline_stat"
#     # "fixed05_stattest"
#     # "partial5"
#     )
# buildlist=("fixed20" "baseline" "fixed10"  "partial10" "fixed10" "fixed10" "fixed05" "partial15" "partial20" "partial10")
# suffixlist=("fixed20" "baseline"  "fixed10a" "partial10a" "fixed10b" "fixed10c" "fixed05" "partial15" "partial20" "partial10b")
# buildlist=("partial10" "baseline" "partial15"  "partial10" "partial15" "partial20" "partial20" "partial15" "partial20" "partial10")
# suffixlist=("partial10c" "baseline"  "partial15a" "partial10a" "partial15c" "partial20a" "partial20c" "partial15b" "partial20b" "partial10b")
# buildlist=("partial15")
# suffixlist=("partial15")
# buildlist=("baseline_stat")
# suffixlist=("baseline_stat")
# benchmark=("../Benchmark/2024/benchmarks/")
# benchmark=("../FPBenchmark/jkubenchall/")
# benchmark=("../FPBenchmark/bvsmts/")
# benchmark=("../FPBenchmark/bvmult/")
# benchmark=("../FPBenchmark/bvmult_nonlinear/")
# benchmark=("../FPBenchmark/bvadd/")
# benchmark=("../FPBenchmark/bvaddjku_arc1/")
# benchmark=("../FPBenchmark/bvaddjku/")
benchmark=(
# "../FPBenchmark/mitercircuits/all/"
# "../FPBenchmark/miters/hwmcc12/opt/"
# "../FPBenchmark/nbitadd_translation/"
# "../FPBenchmark/nbitadd/add_assoc/"
# "../FPBenchmark/nbitadd/mixed/"
# "../FPBenchmark/nbitadd/add_commu/"
# "../FPBenchmark/nbitmult/mult_assoc/"
# "../FPBenchmark/nbitmult/15bitcommu/"
# "../FPBenchmark/nbitadd/vanilla/"
"../FPBenchmark/op/"
# "../FPBenchmark/nbitmult/statcommu/"
# "../FPBenchmark/nbitmult/mult_commu/"
# "../FPBenchmark/nbitmult/vanillaasso/"

)

# benchmark=("../FPBenchmark/nbitadd_translation/")

# benchmark=("2333../FPBenchmark/fpsmts/")
# benchmark=("../FPBenchmark/cppvsbv_smts/")
# benchmark=("../CryptoBenchmark/ascon/" "../CryptoBenchmark/soos/")
# benchmark=("../CryptoBenchmark/soos2/")
# benchmark=("../CryptoBenchmark/float2/")
# benchmark=("../CryptoBenchmark/soos/")
# benchmark=("../float4/")
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

        # for (( jj=100; jj<200;)); do
        # for (( jj=30; jj<100;)); do
            # jj=900
            # jobid=$(sbatch --priority 1 -o ./Outputs/output_%A_%a_$jj.out --array=1-${num_tasks} ./RemoteScripts/array_submit_solver.sh $build ${suffix}_${jj} $benchmark_path "--tick_limit_reset" $jj | awk '{print $4}')
            # echo "Submitted job with ID: $jobid" ${suffix}_${jj}
            # sleep 1s
            # sbatch --dependency=afterok:$jobid -o ./Outputs/log_single_process/$suffix.log --priority 0 ./RemoteScripts/submit_python_log_single.sh $suffix
            # jj=$((jj+300))
        # done

        jobid=$(sbatch --priority 0 -o ./Outputs/output_%A_%a.out --array=1-${num_tasks} ./RemoteScripts/array_submit_solver.sh $build ${suffix} $benchmark_path | awk '{print $4}')
        echo "Submitted job with ID: $jobid" ${suffix}
    done
done
