import glob
import utils.states as states
import json         
import os
import re
from tqdm import tqdm

def ParseBits(folder, name, try_use_cache = False):
    #Relaxed parsing here
    file_name = f'{folder}*.{name}*log'
    cache_name = f'{folder}/BitsGroup.json'
    log_files = glob.glob(file_name)
    if len(log_files) == 0:
        print(f"ParseBits: not matched any log with {name}")
        return None
    bits=[]
    result_table={}
    if try_use_cache and os.path.isfile(cache_name):
        with open(cache_name, "r") as file:
            result_table = json.load(file)
            bits = result_table["bits"]
        if bits and len(bits) != 0:
            return bits
    else:
        for filename in log_files:
            pattern = r'\.bits_(\d+)\.'
            # pattern = r'add_(\d+)_'
            match = re.search(pattern,filename)
            # matches = re.findall(filename, text)
            # print(filename)
            
            if match:
                bstr=match.group(1)
                # if len(bstr) > 3:
                #     bstr = bstr[0:3]
                bit = int(bstr)
                bits.append(bit)
        with open(cache_name, "w") as file:
            result_table["bits"] = bits
            json.dump(result_table, file)
        
    return bits

def GetAllKeys(folder, name):
    keys = []
    file_name = f'{folder}*{name}.log'
    log_files = glob.glob(file_name)
    for filename in log_files:
        basename = os.path.basename(filename)
        # key = basename[0:32]
        key = basename
        # parts = key.split('.')
        # key = parts[0]
        keys.append(key)
    return keys

def GetDataForBit(folder,name, bit, use_cache = False):
    return GetData(folder,name, use_cache, bit)

def GetData(folder,name, use_cache = False, bit=None):
    if name in states.refreshed:
        use_cache = True
    else:
        states.refreshed.append(states.refreshed)
    # file_name = f'{folder}*.{name}.*log'
    # if bit:
    #     file_name = f'{folder}*{name}.*.log'
    # else:
    file_name = f'{folder}*{name}.*log'
    cache_name = f'{folder}/{name}.solverCache.json'
    log_files = glob.glob(file_name)
    file_counted = 0
    if bit:
        None
        # print(f'{file_name} matched {len(log_files)} for bit {bit}')
        cache_name = f'{folder}/{name}.solverCache_{bit}.json'
    else:
        print(f'{file_name} matched {len(log_files)}')
    if len(log_files) == 0:
        return None,None,None,None
    states.matched = len(log_files)
    data_for_this_solver = []
    sum_time = 0.0
    instance_mem_map = {}
    data_for_this_solver,instance_time_map,par2 = [],{},-1
    if use_cache and os.path.isfile(cache_name):
        with open(cache_name, "r") as file:
            result_table = json.load(file)
            data_for_this_solver = result_table["data"]
            instance_time_map = result_table["map"]
            par2 = result_table["par2"]
            instance_mem_map = {}
            # instance_mem_map = result_table["mem"]
    else:
        for filename in tqdm(log_files):
            basename = os.path.basename(filename)
            if bit:
                if f"bits_{bit}." not in basename:
                # if f"bits_{bit}." not in basename:
                # if f"add_{bit}_" not in basename:
                    # print(basename, f"bits_{bit}")
                    continue
            file_counted += 1
            # print(basename)
            # key = basename[0:32]
            # key = basename[0:32]
            key = basename
            # parts = key.split('.')
            # key = parts[0]
            solved = False
            
            # if process_stat:
            #     average_glue_size, average_number_count = getstat(filename)
            #     instance_avglbd_map[key] = average_glue_size
            #     instance_avgclength_map[key] = average_number_count
            with open(filename, 'rb') as file:
                # print(f"processing {filename}")
                file.seek(0, 2)
                position = file.tell()
                line = b''
                linecnt=0
                phase=0 # 0 for time, 1 for mem
                while position >= 0 and linecnt <= 500:        
                    # print(linecnt)
                    file.seek(position)
                    char = file.read(1)
                    if char == b'\n' and line:
                        linecnt+=1
                        decoded_line = line.decode('utf-8')
                        if "raising signal" in decoded_line:
                            print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!! {filename}")
                            continue
                            # break
                        if "mylog" in decoded_line:
                            continue
                            # assert(0)
                # for line in reversed(file.readlines()):
                    # i+=1
                        # print(f"{decoded_line}\n")
                        if phase ==1:
                            if "maximum-resident-set-size:" in decoded_line:
                                match = re.search(r'(\d*)\s+MB', decoded_line)
                                if match:
                                    time = float(match.group(1))
                                    # sum_time += time
                                    # solved = True
                                    # data_for_this_solver.append(time)
                                    instance_mem_map[key] = time
                                    break
                            
                            break
                        if "process-time" in decoded_line or "total process time" in decoded_line:
                            match = re.search(r'(\d+\.?\d*)\s+seconds', decoded_line) or re.search(r'total process time[^:]*:\s*([0-9]+(?:\.[0-9]+)?)\s*seconds', decoded_line)
                            if match:
                                # print(basename)
                                time = float(match.group(1))
                                sum_time += time
                                solved = True
                                data_for_this_solver.append(time)
                                instance_time_map[key] = time
                                phase = 1
                            
                        if "CPU time" in decoded_line in decoded_line:
                            match = re.search(r'CPU time[^:]*:\s*([0-9]+(?:\.[0-9]+)?)\s*s', decoded_line)
                            if match:
                                # print(basename)
                                time = float(match.group(1))
                                sum_time += time
                                solved = True
                                data_for_this_solver.append(time)
                                instance_time_map[key] = time
                                phase = 1
                        line = b''
                    else:
                        line = char + line  # 将字节追加到当前行内容
                    position -= 1
                if not solved:
                    sum_time += 10000.0 
                    # sum_time += 5000.0 
        
        if file_counted > 0:
            # print(f"par2 calculatedby {sum_time}/{file_counted}")
            par2 = sum_time / file_counted
        else:
            par2 = None
            
        with open(cache_name, "w") as file:
            result_table = {}
            result_table["data"] = data_for_this_solver
            result_table["map"] = instance_time_map
            result_table["par2"] = par2
            result_table["mem"] = instance_mem_map
            json.dump(result_table, file)
    if not bit:
        print(f"Par2 {par2}, #solved {len(data_for_this_solver)}")
    # print(len(instance_time_map))
    return data_for_this_solver,instance_time_map,par2,instance_mem_map