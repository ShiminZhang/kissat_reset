import glob
import utils.states as states
import json         
def ParseBits(folder, name, use_cache = False):
    file_name = f'{folder}*{name}.log'
    cache_name = f'{folder}/BitsGroup.json'
    log_files = glob.glob(file_name)
    if len(log_files) == 0:
        return None
    bits=[]
    result_table={}
    if use_cache:
        with open(cache_name, "r") as file:
            result_table = json.load(file)
            bits = result_table["bits"]
    else:
        for filename in log_files:
            match = re.search(r'(\d+\.?\d*)\s+seconds', filename)
            
    return bits

def GetAllKeys(folder, name):
    keys = []
    file_name = f'{folder}*{name}.log'
    log_files = glob.glob(file_name)
    for filename in log_files:
        basename = os.path.basename(filename)
        # key = basename[0:32]
        key = basename
        parts = key.split('.')
        key = parts[0]
        keys.append(key)
    return keys


def GetData(folder,name, use_cache = False):
    if name in states.refreshed:
        use_cache = True
    else:
        states.refreshed.append(states.refreshed)
    file_name = f'{folder}*{name}.log'
    cache_name = f'{folder}/{name}.solverCache.json'
    log_files = glob.glob(file_name)
    print(f'{folder}.*{name}.*.log matched {len(log_files)}')
    if len(log_files) == 0:
        return None,None,None
    states.matched = len(log_files)
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
            # print(basename)
            # key = basename[0:32]
            # key = basename[0:32]
            key = basename
            parts = key.split('.')
            key = parts[0]
            solved = False
            # if process_stat:
            #     average_glue_size, average_number_count = getstat(filename)
            #     instance_avglbd_map[key] = average_glue_size
            #     instance_avgclength_map[key] = average_number_count
            with open(filename, 'rb') as file:
                file.seek(0, 2)  # 将文件指针移动到文件末尾
                position = file.tell()  # 获取文件总长度（位置）
                line = b''
                linecnt=0
                while position >= 0 and linecnt <= 50:        
                    file.seek(position)  # 将指针移动到当前位置
                    char = file.read(1)  # 读取一个字节
                    if char == b'\n' and line:  # 如果遇到换行符，说明读到了一行
                        linecnt+=1
                        decoded_line = line.decode('utf-8')  # 倒序并解码
                # for line in reversed(file.readlines()):
                    # i+=1
                        # print(f"{decoded_line}\n")
                        if "process-time" in decoded_line or "total process time" in decoded_line:
                            match = re.search(r'(\d+\.?\d*)\s+seconds', decoded_line) or re.search(r'total process time[^:]*:\s*([0-9]+(?:\.[0-9]+)?)\s*seconds', decoded_line)
                            if match:
                                time = float(match.group(1))
                                sum_time += time
                                solved = True
                                data_for_this_solver.append(time)
                                instance_time_map[key] = time
                                break
                        line = b''
                    else:
                        line = char + line  # 将字节追加到当前行内容
                    position -= 1
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