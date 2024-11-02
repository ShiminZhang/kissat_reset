import glob
import re
import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
import json         
                    
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
            key = basename[0:10]
            with open(filename, 'r') as file:
                solved = False
                for line in file:
                    if "process-time" in line:
                        match = re.search(r'(\d+\.?\d*)\s+seconds', line)
                        if match:
                            time = float(match.group(1))
                            sum_time += time
                            solved = True
                            data_for_this_solver.append(time)
                            instance_time_map[key] = time
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
            json.dump(result_table, file)
    
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process log files.')
    parser.add_argument('--UseCache', action='store_true', help='Enable cache usage')
    args = parser.parse_args()
    use_cache_flag = args.UseCache
    print(use_cache_flag)
    plt.figure(figsize=(10, 6))
    kissat_log_path = "../../Benchmark/2024/benchmarks/kissat/"

    def CompareAndShowExcell(base_tag, better_tag):
        _,base,_ = GetData(kissat_log_path,base_tag,use_cache_flag)
        _,better,_ = GetData(kissat_log_path,better_tag,use_cache_flag)
        # better["5e5fe73a2e"]
        result = []
        for key in base.keys():
            if key in better.keys():
                if better[key] < base[key]:
                    result.append(key)
            else:
                print(key)
        # print(result)
        return result
    
    def wrapped_plot(tag):
        GetDataAndPlot(kissat_log_path, tag, use_cache_flag)
    # wrapped_plot("mab")
    wrapped_plot("baseline")
    wrapped_plot("fixed05")
    # wrapped_plot("fixed02")
    # wrapped_plot("fixed03")
    # wrapped_plot("fixed04")
    # wrapped_plot("fixed06")
    # wrapped_plot("fixed07")
    # wrapped_plot("fixed08")
    # wrapped_plot("fixed09")
    # wrapped_plot("mlr")
    # wrapped_plot("resetactinfocus")
    CompareAndShowExcell("baseline", "fixed05")
    plt.xlabel('Cumulative Time (seconds)')
    plt.ylabel('Number of Problems Solved')
    plt.title('SAT2024')
    plt.legend()
    plt.grid(True)
    plt.savefig("./test.png")
    
    
