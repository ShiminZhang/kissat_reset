import numpy as np
from scipy.stats import pearsonr

# 读取文件内容
def read_log_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

# 提取ticks数据和restart的位置
def extract_ticks_and_restarts(data):
    ticks = []
    restart_indices = []
    
    for i, line in enumerate(data):
        if 'ticks during propagation' in line:
            ticks.append(int(line.split()[-1]))
        elif 'restart' in line:
            restart_indices.append(len(ticks))
    
    return ticks, restart_indices

# 计算每个restart前后ticks配对的相关性
def calculate_restart_pair_correlations(ticks, restart_indices):
    correlations = []
    prev_ticks = []
    next_ticks = []
    print(len(ticks))
    # print(restart_indices)
    # 遍历每个restart，计算前后ticks配对的相关性
    for restart_index in restart_indices:
        # 确保restart前后有有效数据
        if 0 < restart_index < len(ticks) - 1:
            prev_ticks.append(ticks[restart_index - 1])
            next_ticks.append(ticks[restart_index])
            
            # 计算相关性（使用Pearson相关系数）
    prev_ticks = np.array(prev_ticks)
    next_ticks = np.array(next_ticks)
    print("avg ticks before restart: ",np.mean(prev_ticks))
    print("avg ticks after restart: ",np.mean(next_ticks ))
    print("avg ticks reduced: ",np.mean(prev_ticks - next_ticks ))
    [ print(x) for x in zip(prev_ticks, next_ticks)]
    
    # print(len(prev_ticks), len(next_ticks))
    corr, _ = pearsonr(prev_ticks, next_ticks)
    return corr

def main():
    file_path = '3reset.log'  # 请替换为您的日志文件路径
    log_data = read_log_file(file_path)
    
    # 提取ticks和restart信息
    ticks, restart_indices = extract_ticks_and_restarts(log_data)
    
    # 计算所有restart前后ticks配对的总相关性
    total_correlation = calculate_restart_pair_correlations(ticks, restart_indices)
    
    # 输出结果
    if total_correlation is not None:
        print(f'Total correlation of all restart tick pairs: {total_correlation}')
    else:
        print('No valid tick pairs for correlation.')

if __name__ == '__main__':
    main()
