import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import utils.states as states
from utils.utils import GetData,ParseBits
import numpy as np

def Plot(data : list, solver_name):
    data.sort()
    y_array = np.arange(1, len(data) + 1)
    x_array = np.array(data)
    
    plt.plot(x_array, y_array, label=f'{solver_name}')

def GetDataAndPlot(LogPath, tag, use_cache_flag):
    data,map,par2 = GetData(LogPath, tag, use_cache_flag)
    if not data:
        print(f"no data for {tag}")
        return
    Plot(data, tag)
    return len(data),par2

def PlotScaling(LogPath, tag, use_cache_flag):
    data,map,par2 = GetData(LogPath, tag, use_cache_flag)
    if not data:
        print(f"no data for {tag}")
        return
    bits = ParseBits(LogPath)
    for bit in bits:
        #plot for that tag
        

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