#!/bin/bash                                                    
#SBATCH --time=0-0:0:5300                                                      
#SBATCH --account=def-vganesh   

buildlist=(
    # "fixed05_decay10"
    # "baseline_decay10"
    # "partial10_decay10"
    # "fixed05nodump"
    # "baselinenodump"
    # "fixed05_decay20"
    # "baseline_decay20"
    # "fixed05_decay30"
    # "baseline_decay30"
    # "partial10_decay30"
    # "fixed05_decay40"
    # "baseline_decay40"
    # "fixed05_decay50"
    # "baseline_decay50"
    # "partial10_decay50"
    # "fixed05_decay60"
    # "baseline_decay60"
    # "baseline_decay70"
    # "fixed05_decay70"
    # "partial10_decay70"
    # "baseline_decay80"
    # "fixed05_decay80"
    # "fixed05_decay90"
    # "baseline_decay90"
    # "partial10_decay90"
    # "kissat_nopreprocessing_decay25"
    # "kissat_nopreprocessing_decay50"
    # "kissat_nopreprocessing_decay75"
    # "kissat_nopreprocessing_default"
    "minisat_decay25"
    "minisat_decay50"
    "minisat_decay75"
    "minisat_default"
    )
suffixlist=(
    # "fixed05_decay10"
    # "baseline_decay10"
    # "partial10_decay10"
    # "fixed05nodump"
    # "baselinenodump"
    # "fixed05_decay20"
    # "baseline_decay20"
    # "fixed05_decay30"
    # "baseline_decay30"
    # "partial10_decay30"
    # "fixed05_decay40"
    # "baseline_decay40"
    # "fixed05_decay50"
    # "baseline_decay50"
    # "partial10_decay50"
    # "fixed05_decay60"
    # "baseline_decay60"
    # "baseline_decay70"
    # "fixed05_decay70"
    # "partial10_decay70"
    # "baseline_decay80"
    # "fixed05_decay80"
    # "fixed05_decay90"
    # "baseline_decay90"
    # "partial10_decay90"
    # "kissat_nopreprocessing_decay25"
    # "kissat_nopreprocessing_decay50"
    # "kissat_nopreprocessing_decay75"
    # "kissat_nopreprocessing_default"
    "minisat_decay25"
    "minisat_decay50"
    "minisat_decay75"
    "minisat_default"
    )
# buildlist=(
#     # "f05a"
#     # # "fixed05"
#     # "fixed05nodump"
#     # "baseline"
#     # "vanilla_kissat_reset"
#     # "vanilla_kissat"
# #     # "baseline_nocongruence"
# #     # "fixed05_nocongruence"
# #     # "fixed05_stat"
# #     # "fixed10_stat"
# #     # "baseline_stat"
# #     # "fixed05_stattest"
# #     "stattest"
# #     "dumptest"
# #     "stattest"
# #     "dumptest"
# #     # "partial5"
#     )

# suffixlist=(
#     # "kissat_reset"
#     # "kissat"
#     # "f05a"
#     # # "f05b"
#     # "f05c"
#     # "b1"
#     # "fixed05"
#     # "baseline"
#     # "baseline_nocongruence"
#     # "fixed05_nocongruence"
#     # "fixed05_stat"
#     # "fixed10_stat"
#     # "stattest1"
#     # "dumptest1"
#     # "stattest2"
#     # "dumptest2"
#     # "baseline_stat"
#     # "fixed05_stattest"
#     # "partial5"
#     )
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
# "../FPBenchmark/nbitmult/commu/"
# "../FPBenchmark/nbitadd/addition/"
"../FPBenchmark/opeasy/"
"../FPBenchmark/gop/"
"../FPBenchmark/4regular_gop/"
"../FPBenchmark/6regular_gop/"
"../FPBenchmark/8regular_gop/"
# "../SATBenchmark/"
# "../FPBenchmark/opext/"
# "../FPBenchmark/opfull/"
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

        jobid=$(sbatch --priority 0 --constraint=cascade -o ./Outputs/output_%A_%a.out --array=1-${num_tasks} ./RemoteScripts/array_submit_solver.sh $build ${suffix} $benchmark_path | awk '{print $4}')
        echo "Submitted job with ID: $jobid" ${suffix}
    done
done
