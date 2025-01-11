
def GetStatFromFolder(folder,name):
    file_name = f'{folder}*{name}.log'
    cache_name = f'{folder}/{name}.solverCache.json'
    log_files = glob.glob(file_name)
    print(f'Collecting Stat from {folder}.*{name}.*.log | matched {len(log_files)}')
    if len(log_files) == 0:
        return None,None
    instance_time_map = {}
    instance_avglbd_map = {}
    instance_avgclength_map = {}

    for filename in log_files:
            basename = os.path.basename(filename)
            # print(basename)
            # key = basename[0:32]
            
            # key = basename[0:32]
            key = basename
            parts = key.split('.')
            key = parts[0]
            solved = False
            average_glue_size, average_number_count = getstat(filename)
            instance_avglbd_map[key] = average_glue_size
            instance_avgclength_map[key] = average_number_count
    return instance_avglbd_map,instance_avgclength_map

    
def extract_glue_data(file_path):
    glue_data = []
    with open(file_path, 'r') as file:
        for line in file:
            if "garbage" in line:
                continue
            match = re.search(r"redundant glue (\d+) clause\[\d+\](.*)", line)
            if match:
                glue_size = int(match.group(1))
                numbers = match.group(2).strip().split()
                number_count = len(numbers)
                glue_data.append((glue_size, number_count))
    return glue_data

def calculate_averages(glue_data):
    if not glue_data:
        return (0, 0)

    total_glue_size = sum(glue_size for glue_size, _ in glue_data)
    total_number_count = sum(number_count for _, number_count in glue_data)
    average_glue_size = total_glue_size / len(glue_data)
    average_number_count = total_number_count / len(glue_data)

    return (average_glue_size, average_number_count)

def getstat(file_path):
    result = extract_glue_data(file_path)
    average_glue_size, average_number_count = calculate_averages(result)
    # print(average_glue_size, average_number_count)
    with open(f"{file_path}.stat", "w") as f:
        f.write(str((average_glue_size,average_number_count)))
    return average_glue_size, average_number_count