from utils.utils import GetAllKeys,GetData
from utils.plotting import GetDataAndPlot,PlotScaling,GetDataAndPlotMem
import utils.states as states
import pandas as pd
from collections import Counter
import sqlite3    
import matplotlib.cm as cm
import numpy as np

tag_count = 0

def ClearTagCount():
    global tag_count
    tag_count = 0

def query_hashes_par2(par2_map, hash_tag="Frequency"):
    hashes = list(par2_map.keys())
    conn = sqlite3.connect('./meta.db')
    cursor = conn.cursor()
    placeholders = ','.join('?' for _ in hashes)
    query = f"SELECT hash, family FROM features WHERE hash IN ({placeholders})"
    results = cursor.execute(query, hashes).fetchall()
    hash_family_mapping = {hash_: family for hash_, family in results}
    conn.close()
    family_par2_mapping = {family: 0 for _,family in results}
    for key in hash_family_mapping.keys():
        family_par2_mapping[hash_family_mapping[key]] += par2_map[key]
        
    value_counts = Counter(hash_family_mapping.values())
    family_normpar2_mapping = { key: (float(family_par2_mapping[key]) / float(value_counts[key])) for _,key in results }
    df = pd.DataFrame(family_normpar2_mapping.items(), columns=['Value', hash_tag])
    return df

def query_hashes(hashes, hash_tag="Frequency"):
    conn = sqlite3.connect('./meta.db')
    cursor = conn.cursor()
    placeholders = ','.join('?' for _ in hashes)
    query = f"SELECT hash, family FROM features WHERE hash IN ({placeholders})"
    results = cursor.execute(query, hashes).fetchall()
    hash_family_mapping = {hash_: family for hash_, family in results}
    conn.close()
    value_counts = Counter(hash_family_mapping.values())
    df = pd.DataFrame(value_counts.items(), columns=['Value', hash_tag])
    return df

def GetMergedDF(result,legend_better,legend_worse):
    df1 = query_hashes(list(result["better"].keys()), legend_better)
    df2 = query_hashes(list(result["worse"].keys()), legend_worse)
    merged_df = pd.merge(df1, df2, on='Value', how='outer').fillna(0)
    merged_df[legend_better] = merged_df[legend_better].astype(int)
    merged_df[legend_worse] = merged_df[legend_worse].astype(int)
    return merged_df

def CompareTime(base_tag, better_tag):
    _,base,_,_ = GetData(states.kissat_log_path,base_tag,states.use_cache_flag)
    _,better,_,_ = GetData(states.kissat_log_path,better_tag,states.use_cache_flag)
    result = {}
    result["better"] = {}
    result["worse"] = {}
    for key in base.keys():
        if key in better.keys():
            if better[key] < base[key]:
                result["better"][key] = base[key] - better[key]
            elif better[key] >= base[key]:   
                result["worse"][key] = base[key] - better[key] 
    return result

def ConstructVirtualBest(tags: list):
    others = {}
    missing = []
    for tag in tags:
        _,current,_,_ = GetData(states.kissat_log_path,tag,states.use_cache_flag)
        if not current:
            missing.append(tag)
            continue
        others[tag] = current
    for tag in missing:
        tags.remove(tag)
    keys = GetAllKeys(states.kissat_log_path,"baseline")
    best_data = []
    for key in keys:
        best = 999999
        for tag in tags:
            if tag in others.keys() and key in others[tag].keys() and others[tag][key] < best:
                best = others[tag][key]
        if best != 999999:
            best_data.append(best)
    print(f"virtualbest: {len(best_data)}")
    Plot(best_data, "virtualbest")

def CompareAndShowExcell(base_tag, better_tag):
    result = CompareTime(base_tag, better_tag)
    legend_better = f"A win"
    legend_worse = f"B win"
    
    merged_df = GetMergedDF(result,legend_better,legend_worse)
    
    DrawDF(merged_df,f"Catagories_{better_tag}(A)_vs_{base_tag}(B).png", better_tag,base_tag)
    return

def CompareByNormalPar2(base_tag, better_tag):
    _,base,_,_ = GetData(states.kissat_log_path,base_tag,states.use_cache_flag)
    _,better,_,_ = GetData(states.kissat_log_path,better_tag,states.use_cache_flag)
    result = {}
    result["better"] = {}
    result["base"] = {}
    keys = GetAllKeys(states.kissat_log_path,"baseline")
    print(len(keys))
    for key in keys:
        result["better"][key] = 10000
        result["base"][key] = 10000
        if key in better.keys():
            result["better"][key] = better[key]
        if better[key] == 10000:
            print(f"{better_tag} not contain {key}")
        if key in base.keys():
            result["base"][key] = base[key]
        else:
            print(f"{bettebase_tagr_tag} not contain {key}")

    
    legend_better = f"A normalized par2"
    legend_worse = f"B normalized par2"
    
    df1 = query_hashes_par2(result["better"], legend_better)
    df2 = query_hashes_par2(result["base"], legend_worse)
    merged_df = pd.merge(df1, df2, on='Value', how='outer').fillna(0)
    merged_df[legend_better] = merged_df[legend_better].astype(int)
    merged_df[legend_worse] = merged_df[legend_worse].astype(int)
    DrawDF(merged_df,f"Catagories_{better_tag}(A)_vs_{base_tag}(B).png", better_tag,base_tag)
    # print(merged_df)
    # print(df1)        
    # print(df2)        

def WrappedPlot(tag):
    print(f"Plotting for {tag} in {states.kissat_log_path}")
    global tag_count
    values = np.linspace(0, 1, states.num_lines)
    # print(values)
    # assert(0)
    cmap = cm.get_cmap('tab20')
    # color = cm.viridis(values[tag_count])
    color = cmap(values[tag_count])
    # print(color)
    tag_count += 1
    GetDataAndPlot(states.kissat_log_path, tag, states.use_cache_flag,color)
    
def WrappedPlotMem(tag):
    print(f"Plotting mem for {tag} in {states.kissat_log_path}")
    global tag_count
    values = np.linspace(0, 1, states.num_lines)
    color = cm.viridis(values[tag_count])
    tag_count += 1
    GetDataAndPlotMem(states.kissat_log_path, tag, states.use_cache_flag,color)
    
def WrappedPlotScaling(tag,plotPar2=False):
    print(f"Plotting Scaling for {tag} in {states.kissat_log_path}")
    global tag_count
    values = np.linspace(0, 1, states.num_lines)
    cmap = cm.get_cmap('tab20')
    color = cmap(values[tag_count])
    tag_count += 1
    PlotScaling(states.kissat_log_path, tag, states.use_cache_flag,plotPar2,color)
    
def HowMuchBetter(base_tag, better_tag):
    _,base,_,_ = GetData(states.kissat_log_path,base_tag,states.use_cache_flag)
    _,better,_,_ = GetData(states.kissat_log_path,better_tag,states.use_cache_flag)
    result = CompareTime(base_tag, better_tag)
    keys = GetAllKeys(states.kissat_log_path,"baseline_stat")
    print(len(keys))
    basemiss=[]
    bettermiss=[]
    for key in keys:
        if key in better.keys():
            None
        else:
            bettermiss.append(key)
        if key in base.keys():
            None
        else:
            basemiss.append(key)
    for key in keys:
        if key in bettermiss and key not in basemiss:
            print(f"{better_tag} not contain {key}")
        
        if key not in bettermiss and key in basemiss:
            print(f"{base_tag} not contain {key}")
    betters = np.array([result["better"][k] for k in result["better"].keys()])
    worses = [result["worse"][k] for k in result["worse"].keys()]
    print("_________________________________________")
    print(f"{better_tag} better at {len(betters)} intances and is {np.sum(betters) / len(betters)} seconds better on avg")
    print("_________________________________________")
    print(f"{better_tag} worse at {len(worses)} intances and is {np.sum(worses) / len(worses)} seconds worse on avg")