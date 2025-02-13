# import glob
# import re
import argparse
# import os
# import sqlite3    
# from collections import Counter
# import pandas as pd
from utils.interface import WrappedPlot,HowMuchBetter,CompareByNormalPar2,WrappedPlotScaling,WrappedPlotMem
import utils.states as states
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
# states.refreshed=[]
# states.matched=0
# process_stat=True
# def GetAllKeys(folder, name):
#     keys = []
#     file_name = f'{folder}*{name}.log'
#     log_files = glob.glob(file_name)
#     for filename in log_files:
#         basename = os.path.basename(filename)
#         # key = basename[0:32]
#         key = basename
#         parts = key.split('.')
#         key = parts[0]
#         keys.append(key)
#     return keys


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process log files.')
    parser.add_argument('--UseCache', action='store_true', help='Enable cache usage')
    parser.add_argument('--PlotScaling', action='store_true', help='Plot bit scaling plot instead of cactus')
    parser.add_argument('--PlotScalingPar2', action='store_true', help='Plot bit scaling plot instead of cactus')
    parser.add_argument('--PlotMem', action='store_true', help='Plot bit scaling plot instead of cactus')
    args = parser.parse_args()
    states.use_cache_flag = args.UseCache
    print(states.use_cache_flag)
    plt.figure(figsize=(10, 6))
    benchmark_name = "statcommu"
    CollectStat = False
    arc=None
    # arc=1
    # CollectStat = True
    # mult_commu_arc1
    log_paths = {
        "SAT2024" : "../Benchmark/2024/benchmarks/",
        "test" : "./Benchmark_test/",
        "float4" : "../float4/",
        "float3" : "../float3/",
        "jkubenchall" : "../FPBenchmark/jkubenchall/",
        "float2" : "../CryptoBenchmark/float2/",
        "float1" : "../CryptoBenchmark/float/",
        "nbitaddassoc" : "../FPBenchmark/nbitadd/add_assoc/",
        "nbitaddall" : "../FPBenchmark/nbitadd/mixed/",
        "nbitaddva" : "../FPBenchmark/nbitadd/vanilla/",
        "nbitmultall" : "../FPBenchmark/nbitmult/mixed/",
        "nbitmultva" : "../FPBenchmark/nbitmult/vanilla/",
        "nbitmultsingle" : "../FPBenchmark/nbitmult/vanilla_arc1/",
        "nbitmultvacommu" : "../FPBenchmark/nbitmult/vanillacommu/",
        "nbitmultvaasso" : "../FPBenchmark/nbitmult/vanillaasso/",
        "nbitaddcommu" : "../FPBenchmark/nbitadd/add_commu/",
        "nbitmultassoc" : "../FPBenchmark/nbitmult/mult_assoc/",
        "nbitmultcommu" : "../FPBenchmark/nbitmult/mult_commu/",
        "15bitcommu" : "../FPBenchmark/nbitmult/15bitcommu/",
        "statcommu" : "../FPBenchmark/nbitmult/statcommu/",
        "op" : "../FPBenchmark/op/",
        "bvsmt" : "../FPBenchmark/bvsmts/",
        "fpsmt" : "../FPBenchmark/fpsmts/",
        "bvmult" : "../FPBenchmark/bvmult/",
        "bvmult_nonlinear" : "../FPBenchmark/bvmult_nonlinear/",
        "mitercircuits" : "../FPBenchmark/mitercircuits/all/",
        "miters" : "../FPBenchmark/miters/hwmcc12/opt/",
        "mitersnonopt" : "../FPBenchmark/miters/hwmcc12/nonopt/",
        "bvadd" : "../FPBenchmark/bvadd/",
        "bvaddxor" : "../FPBenchmark/bvaddxor/",
        "nbitadd_translation" : "../FPBenchmark/nbitadd_translation/",
        "bvaddjku" : "../FPBenchmark/bvaddjku/",
        "cppvsbv_smts" : "../FPBenchmark/cppvsbv_smts/"
    }
    states.kissat_log_path = log_paths[benchmark_name]
    if arc:
        states.kissat_log_path = states.kissat_log_path[0:-1] + f"_arc{arc}/" 
    InterestedTags=[
        # "baseline_nocongruence",
        # "fixed05_nocongruence"
        # "fixed05_stat",
        # "fixed05_stattest",
        # "stattest1",
        # "dumptest1",
        # "stattest2",
        # "dumptest2",
        # "baseline_stat",
        # "reset05decay10",
        # "reset05decay20",
        # "reset05decay30",
        # "reset05decay40",
        # "reset05decay50",
        # "reset05decay60",
        # "reset05decay70",
        # "reset05decay80",
        # "reset05decay90",
        
        "baselinedump",
        "fixed05dump",
        # "baselinenodump",
        # "fixed05nodump"
        
        # "baseline",
        # "fixed05"
                   ]
    OverrideFigureTitle={
        "bvaddjku" : "N-bit addition translation"
    }
    # InterestedTags=["baseline",
    #                 "fixed10c","fixed40",
    #                "fixed10", "fixed20", "fixed05",
    #                "fixed30","fixed80",
    #                "fixed60","fixed70",
    #                "fixed10a","fixed10b","fixed15",
    #                "fixed50", 
    #                "partial10a",
    #                "partial15",
    #                "partial10b","partial15","partial20"
    #                ]
    
    ConstructVBFlag = False
    print(f"checking {states.kissat_log_path}")
    for tag in InterestedTags:
        if args.PlotScalingPar2:
            WrappedPlotScaling(tag,True)
        elif args.PlotScaling:
            WrappedPlotScaling(tag,False)
        elif args.PlotMem:
            WrappedPlotMem(tag)
        else:
            WrappedPlot(tag)
    if ConstructVBFlag:
        ConstructVirtualBest(InterestedTags)
    if CollectStat:
        lbd,leng=GetStatFromFolder(states.kissat_log_path,tag)
        print(lbd)
        print(leng)
    # WrappedPlot("fixed50")
    # ConstructVirtualBest(["fixed05","fixed40", "fixed10", "fixed20","fixed30","fixed15","fixed13","fixed07","fixed50", "baseline"])
    # WrappedPlot("fixed30")
    # HowMuchBetter("baseline", "partial10")
    # HowMuchBetter("baseline", "partial10")
    # HowMuchBetter("baseline", "fixed20")
    # HowMuchBetter("baseline", "fixed30")
    # HowMuchBetter("baseline", "fixed40")
    # HowMuchBetter("baseline", "fixed05")
    # HowMuchBetter("baseline_stat", "fixed05_stat")
    # WrappedPlot("mlr")
    # WrappedPlot("resetactinfocus")
    
    # CompareByNormalPar2("baseline", "partial10")
    # CompareByNormalPar2("baseline", "fixed10")
    # CompareByNormalPar2("baseline", "fixed15")
    # CompareByNormalPar2("baseline", "fixed20")
    # CompareByNormalPar2("baseline", "fixed30")
    # CompareAndShowExcell("baseline", "fixed10")
    benchmark_title = (benchmark_name in OverrideFigureTitle) and OverrideFigureTitle[benchmark_name] or benchmark_name
    if args.PlotScaling:
        PlotName=f"../Figures/{benchmark_name}.scaling.png"
        plt.title(f'Scaling plot for Benchmark: {benchmark_title} ({states.matched} instances in total)')
        plt.legend()
        # plt.xlabel('bits')
        plt.xlabel('elements')
        plt.ylabel('Number of Instances Solved')
    elif args.PlotScalingPar2:
        PlotName=f"../Figures/{benchmark_name}.scalingPar2.png"
        plt.title(f'Scaling plot for Benchmark: {benchmark_title} ({states.matched} instances in total)')
        plt.legend()
        # plt.xlabel('bits')
        plt.xlabel('elements')
        plt.ylabel('Par2 score of the intances with the bits')
        
    elif args.PlotMem:
        PlotName=f"../Figures/{benchmark_name}.mem.png"
        plt.title(f'Mem plot for Benchmark: {benchmark_title} ({states.matched} instances in total)')
        plt.legend()
        plt.xlabel('Memory allocated')
        plt.ylabel('Number of Instances Solved')
    else:
    # CompareAndShowExcell("baseline", "fixed15")
        plt.xlabel('Cumulative Time (seconds)')
        plt.ylabel('Number of Instances Solved')
        # plt.title('SAT2024')
        # plt.title('Benchmark: mixed crypto (557 instances in total)')
        # plt.title('Benchmark: float commutivity (140 instances in total)')
        plt.title(f'Benchmark: {benchmark_title} ({states.matched} instances in total)')
        plt.legend()
        plt.grid(True)
        PlotName = f"../Figures/{benchmark_name}.png"
    plt.savefig(PlotName)
