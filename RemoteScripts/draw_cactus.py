import glob
import re
import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
                    
def GetData(folder,name):
    data = {}
    # for index in range(0,100,10):
    file_name = f'{folder}*{name}*.log'
    log_files = glob.glob(file_name)
    print(f'{folder}.*{name}.*.log matched {len(log_files)}')
    data_for_this_solver = []
    instance_time_map = {}
    for filename in log_files:
        basename = os.path.basename(filename)
        with open(filename, 'r') as file:
            hit = False
            for line in file:
                if "process-time" in line:
                    match = re.search(r'(\d+\.?\d*)\s+seconds', line)
                    if match:
                        time = float(match.group(1))
                        data_for_this_solver.append(time)
                        instance_time_map[basename] = time
                        
                        
    print(len(data_for_this_solver))
    print(len(instance_time_map))
    return data_for_this_solver,instance_time_map

def Plot(data : list, solver_name):
    data.sort()
    y_array = np.arange(1, len(data) + 1)
    x_array = np.array(data)
    
    plt.plot(x_array, y_array, label=f'{solver_name}')
        
if __name__ == "__main__":
    plt.figure(figsize=(10, 6))
    # kissat_baseline_data,kissat_baseline_map = GetData("../../Benchmark/kissat/","baseline")
    # kissat_mlr_data,kissat_mlr_map = GetData("../../Benchmark/kissat/","mlr")
    # kissat_resetactinfocus_data,kissat_resetactinfocus_map = GetData("../../Benchmark/kissat/","resetactinfocus")
    # fix05_data,fix05_map = GetData("../../Benchmark/kissat/","fixed05")
    # fix50_data,fix50_map = GetData("../../Benchmark/kissat/","fixed50")
    
    kissat_baseline_data,kissat_baseline_map = GetData("../../Benchmark/2024/benchmarks/kissat/","baseline")
    kissat_mlr_data,kissat_mlr_map = GetData("../../Benchmark/2024/benchmarks/kissat/","mlr")
    kissat_resetactinfocus_data,kissat_resetactinfocus_map = GetData("../../Benchmark/2024/benchmarks/kissat/","resetactinfocus")
    fix05_data,fix05_map = GetData("../../Benchmark/2024/benchmarks/kissat/","fixed05")
    fix50_data,fix50_map = GetData("../../Benchmark/2024/benchmarks/kissat/","fixed50")
    fix20_data,fix20_map = GetData("../../Benchmark/2024/benchmarks/kissat/","fixed20")
    mab_data,mab_map = GetData("../../Benchmark/2024/benchmarks/kissat/","mab")
    Plot(fix05_data, "fix05")
    Plot(fix50_data, "fix50")
    Plot(kissat_baseline_data, "kissat_baseline")
    Plot(kissat_resetactinfocus_data, "kissat_resetactinfocus")
    Plot(kissat_mlr_data, "kissat_mlr")
    Plot(mab_data, "kissat_mab")
    plt.xlabel('Cumulative Time (seconds)')
    plt.ylabel('Number of Problems Solved')
    plt.title('SAT2023')
    plt.legend()
    plt.grid(True)
    plt.savefig("./test.png")
    
    
