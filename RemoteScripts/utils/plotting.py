import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import utils.states as states
from utils.utils import GetData,ParseBits,GetDataForBit
import numpy as np
from matplotlib.ticker import MaxNLocator

def Plot(data : list, solver_name):
    if data:
        data.append(0)
        data.sort()
        y_array = np.arange(0, len(data))
        x_array = np.array(data)
    else:
        x_array = [0,5300]
        y_array = [0,0]
    plt.plot(x_array, y_array, label=f'{solver_name}')

def GetDataAndPlot(LogPath, tag, use_cache_flag):
    data,map,par2,mem = GetData(LogPath, tag, use_cache_flag)
    if not par2:
        print(f"no data for {tag}")
        return
    Plot(data, tag)
    return len(data),par2

def GetDataAndPlotMem(LogPath, tag, use_cache_flag):
    data,map,par2,mem = GetData(LogPath, tag, use_cache_flag)
    if not data:
        print(f"no data for {tag}")
        return
    print(list(mem.values()))
    Plot(list(mem.values()), tag)
    return len(data),par2

def PlotScaling(LogPath, tag, use_cache_flag, plot_par2_flag):
    bits = ParseBits(LogPath,tag,use_cache_flag)
    if not bits:
        print("Found no bits")
        return
    x_bits=[]
    y_instances=[]
    # print(f"bits: {bits}")
    for bit in set(bits):
        data,map,par2,mem = GetDataForBit(LogPath, tag, bit,use_cache_flag)
        if plot_par2_flag:
            y_instances.append(par2)
        else:
            y_instances.append(len(data))
        x_bits.append(bit)
        # print(par2)
        # print(data)
        print(f"bits{bit} : {len(map)}")
    # print(x_bits)
    # print(sorted(pairs))
    
    pairs = list(zip(x_bits, y_instances))
    filtered_pairs = []
    for pair in pairs:
        # if pair[0] > 170000 and pair[0] < 3770000:
        filtered_pairs.append(pair)
    sorted_pairs = sorted(filtered_pairs)
    # print(sorted_pairs)
    # 提取排序后的 x 和 y 数据
    sorted_x, sorted_y = zip(*sorted_pairs)
    x_indices = range(len(sorted_x))
    plt.plot(x_indices, sorted_y, label=f'{tag}')
    plt.xticks(x_indices,sorted_x)
        

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