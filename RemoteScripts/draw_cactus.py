import glob
import re
import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
import json         
import sqlite3    
from collections import Counter
import pandas as pd
from matplotlib.ticker import MaxNLocator

def GetData(folder,name, use_cache = False):
    file_name = f'{folder}*{name}*.log'
    cache_name = f'{folder}/{name}.solverCache.json'
    log_files = glob.glob(file_name)
    print(f'{folder}.*{name}.*.log matched {len(log_files)}')
    data_for_this_solver = []
    sum_time = 0.0
    instance_time_map = {}
    data_for_this_solver,instance_time_map,par2 = [],{},-1
    if use_cache:
        with open(cache_name, "r") as file:
            result_table = json.load(file)
            data_for_this_solver = result_table["data"]
            instance_time_map = result_table["map"]
            par2 = result_table["par2"]
    else:
        for filename in log_files:
            basename = os.path.basename(filename)
            key = basename[0:32]
            with open(filename, 'r') as file:
                solved = False
                for line in file:
                    if "process-time" in line or "total process time" in line:
                        match = re.search(r'(\d+\.?\d*)\s+seconds', line) or re.search(r'total process time[^:]*:\s*([0-9]+(?:\.[0-9]+)?)\s*seconds', line)
                        if match:
                            time = float(match.group(1))
                            sum_time += time
                            solved = True
                            data_for_this_solver.append(time)
                            instance_time_map[key] = time
                        continue
                if not solved:
                    sum_time += 10000.0 
        
        if len(log_files) > 0:
            par2 = sum_time / len(log_files)
        else:
            par2 = 0
            
        with open(cache_name, "w") as file:
            result_table = {}
            result_table["data"] = data_for_this_solver
            result_table["map"] = instance_time_map
            result_table["par2"] = par2
            # json.dump(result_table, file)
    
    print(par2)
    print(len(data_for_this_solver))
    print(len(instance_time_map))
    return data_for_this_solver,instance_time_map,par2

def Plot(data : list, solver_name):
    data.sort()
    y_array = np.arange(1, len(data) + 1)
    x_array = np.array(data)
    
    plt.plot(x_array, y_array, label=f'{solver_name}')

def GetDataAndPlot(LogPath, tag, use_cache_flag):
    data,map,par2 = GetData(LogPath, tag, use_cache_flag)
    Plot(data, tag)
    return len(data),par2

def DrawDF(InDF, FigureName="DF.png", better="better", base="worse"):
    # print(InDF)
    plt.figure(figsize=(50, 8),dpi=300)
    ax = InDF.set_index('Value').plot(kind='bar', stacked=False, width=0.8)
    plt.title(f'{better}(A) VS {base}(B)', fontsize=12)
    plt.xlabel('Formula Categories', fontsize=8)
    plt.ylabel('Frequency', fontsize=10)
    plt.xticks(rotation=60, ha='right', fontsize=6)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.legend(title='Frequencies', fontsize=10)
    plt.tight_layout()
    plt.savefig(f"/home/s568zhan/scratch/Figures/{FigureName}", bbox_inches='tight',dpi=300)
    # plt.savefig(f"{FigureName}", bbox_inches='tight',dpi=300)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process log files.')
    parser.add_argument('--UseCache', action='store_true', help='Enable cache usage')
    args = parser.parse_args()
    use_cache_flag = args.UseCache
    print(use_cache_flag)
    plt.figure(figsize=(10, 6))
    kissat_log_path = "../Benchmark/2024/benchmarks/"

    def CompareAndShowExcell(base_tag, better_tag):
        _,base,_ = GetData(kissat_log_path,base_tag,use_cache_flag)
        _,better,_ = GetData(kissat_log_path,better_tag,use_cache_flag)
        result = {}
        result["better"] = {}
        # result["diff"] = []
        result["worse"] = {}
        for key in base.keys():
            if key in better.keys():
                if better[key] < base[key]:
                    result["better"][key] = base[key] - better[key]
                elif better[key] > base[key]:   
                    result["worse"][key] = base[key] - better[key] 
            # else:
            #     print(f"{key}")
        # print(result)
        legend_better = f"A win"
        legend_worse = f"B win"
        
        merged_df = GetMergedDF(result,legend_better,legend_worse)
        
        DrawDF(merged_df,f"Catagories_{better_tag}(A)_vs_{base_tag}(B).png", better_tag,base_tag)
        return base,better
    
    def wrapped_plot(tag):
        GetDataAndPlot(kissat_log_path, tag, use_cache_flag)
    # wrapped_plot("mab")
    wrapped_plot("tickEMA_30")
    wrapped_plot("tickEMA_40")
    wrapped_plot("tickEMA_50")
    wrapped_plot("tickEMA_60")
    wrapped_plot("tickEMA_70")
    wrapped_plot("tickEMA_80")
    wrapped_plot("tickEMA_90")
    # wrapped_plot("tickfix_100")
    # wrapped_plot("tickfix_200")
    # wrapped_plot("tickfix_300")
    # wrapped_plot("tickfix_400")
    # wrapped_plot("tickfix_600")
    # wrapped_plot("tickfix_800")
    # wrapped_plot("fixed02")
    # wrapped_plot("fixed03")
    # wrapped_plot("fixed04")
    # wrapped_plot("fixed06")
    # wrapped_plot("fixed07")
    # wrapped_plot("fixed08")
    # wrapped_plot("fixed09")
    # wrapped_plot("mlr")
    # wrapped_plot("resetactinfocus")
    # CompareAndShowExcell("baseline", "fixed05")
    plt.xlabel('Cumulative Time (seconds)')
    plt.ylabel('Number of Problems Solved')
    plt.title('SAT2024')
    plt.legend()
    plt.grid(True)
    plt.savefig("./test.png")
    
    
