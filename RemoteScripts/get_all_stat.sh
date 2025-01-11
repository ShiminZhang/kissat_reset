#!/bin/bash                                                    
#SBATCH --time=0-0:0:5300                                                      
#SBATCH --account=def-vganesh   
benchmakrfolder=("../FPBenchmark/bvsmts/")
benchmakrfolder_l=$(find $benchmakrfolder -name "*.cnf" | wc -l)
taglist=(
    "baseline_stat"
    "fixed05_stat"
)

echo $benchmakrfolder_l
for (( k=1; k<benchmakrfolder_l+1; k++ )); do
    input_cnf=$(find $benchmakrfolder -name "*.cnf" | sed -n "${k}p")
    for (( i=0; i<2; i++ )); do
        tag=${taglist[$i]}
        input_proof=${input_cnf}.$tag.drat
        input_log=${input_cnf}.$tag.log
        sbatch ./RemoteScripts/get_stat.sh $input_cnf $input_proof $input_log
    done
done



# input_cnf="../FPBenchmark/testbvadd/bvadd_30000_2B80695AD48D60CA946DB9A296BF0FDD.smt.cnf"
# input_proof="../FPBenchmark/testbvadd/bvadd_30000_2B80695AD48D60CA946DB9A296BF0FDD.smt.cnf.baseline_stat.drat"
# input_log="../FPBenchmark/testbvadd/bvadd_30000_2B80695AD48D60CA946DB9A296BF0FDD.smt.cnf.baseline_stat.log"

# ./RemoteScripts/get_stat.sh $input_cnf $input_proof $input_log