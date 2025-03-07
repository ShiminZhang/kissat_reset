import re
# import tqdm
def read_cnf_file(cnf_file_path):
    """读取CNF文件并返回每个clause的列表"""
    clauses = []
    with open(cnf_file_path, 'r') as file:
        for line in file:
            # 忽略p和c行
            if line.startswith('p') or line.startswith('c'):
                continue
            # 去掉行尾的零并转换为整数列表
            clause = list(map(str, line.split()))
            if clause:
                clauses.append(clause[:-1])  # 去掉末尾的0
                
    return clauses

def remove_negatives_from_clause(clause):
    """去掉clause中的负号并返回新的clause"""
    return [abs(literal) for literal in clause]

def find_clause_in_log(clause, log_file_path):
    """在log文件中查找对应的clause字符串"""
    # 将clause转换为字符串并排序（因为clause中的数字顺序可能不同）
    normalized_clause = ' '.join(map(str, sorted(clause)))
    # print(f"finding {normalized_clause}")
    # clause_pattern = re.compile(r'\[\d+\]\s+([-\d\s]+)')  # 匹配log行中的数字部分
    
    # clause_pattern = re.compile(r'([-\d\s]+)')  # for .cnf
    # clause_pattern = re.compile(r';\s*([-\d\s]+)$') # for mylog
    clause_pattern = re.compile(r'\]\s*([-\d\s]+)$')  # for kissat dump
    # print(normalized_clause)
    with open(log_file_path, 'r') as file:
        for line in file:
            # 提取log中的clause部分
            match = clause_pattern.search(line)
            if match:
                # print(match)
                log_clause_str = match.group(1).strip()  # 获取数字部分
                # 将log中的数字部分排序后比较
                # print(f"{log_clause_str} |")
                log_clause = ' '.join(sorted(log_clause_str.split(' ')))
                print(f"{log_clause} ||| {normalized_clause} \n")
                # print(log_clause)
                if log_clause == normalized_clause:
                    # print(f"    Found clause {normalized_clause} in log file: {line.strip()}")
                    return True
        return False

def main(cnf_file_path, log_file_path):
    clauses = read_cnf_file(cnf_file_path)
    matched_cores = []
    unmatched_cores = []
    for clause in clauses:
        # normalized_clause = remove_negatives_from_clause(clause)
        # find_clause_in_log(normalized_clause, log_file_path)
        # print(clause)
        if not find_clause_in_log(clause, log_file_path):
            unmatched_cores.append(clause)
            # print(clause)
        else:
            matched_cores.append(clause)
            # print(clause)
        # break
    with open("unmatched_cores.cnf", "w") as f:
        print(len(unmatched_cores))
        for clause in unmatched_cores:
            for l in clause:
                f.write(f"{l} ")
            f.write("\n")
            
    with open("matched_cores.cnf", "w") as f:
        print(len(matched_cores))
        for clause in matched_cores:
            for l in clause:
                f.write(f"{l} ")
            f.write("\n")
            
# cnf_file_path = 'dump.cnf'
cnf_file_path = 'testdump.cnf'
# cnf_file_path = './Benchmark_test/test.cnf'
# log_file_path = 'dump.log'
log_file_path = 'test.log'
# log_file_path = 'irredundant'
# log_file_path = 'glue'
# log_file_path = 'fakelog.log'

main(cnf_file_path, log_file_path)

# clauses=["-1", "-19", "5", "10"]
# print(sorted(clauses))