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
    
    plt.plot(x_array, y_array, label=f'Solver{solver_name}')
        
if __name__ == "__main__":
    plt.figure(figsize=(10, 6))
    kissat_baseline_data,kissat_baseline_map = GetData("../../Benchmark/kissat/","baseline")
    kissat_mlr_data,kissat_mlr_map = GetData("../../Benchmark/kissat/","mlr")
    kissat_resetactinfocus_data,kissat_resetactinfocus_map = GetData("../../Benchmark/kissat/","resetactinfocus")
    Plot(kissat_baseline_data, "kissat_baseline")
    Plot(kissat_mlr_data, "kissat_mlr")
    Plot(kissat_resetactinfocus_data, "kissat_resetactinfocus")
    plt.xlabel('Cumulative Time (seconds)')
    plt.ylabel('Number of Problems Solved')
    plt.title('Solver Performance Over Time')
    plt.legend()
    plt.grid(True)
    plt.savefig("./test.png")
    for k in kissat_baseline_map.keys():
        if k in kissat_mlr_map.keys() and kissat_mlr_map[k] > kissat_baseline_map[k]:
            print(k)
    
    
