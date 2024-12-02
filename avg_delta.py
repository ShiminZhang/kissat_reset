# 打开文件并读取内容
with open('tmp', 'r') as file:
    deltas = []
    for line in file:
        # 查找包含'delta'的行并提取其数值
        if 'delta' in line:
            parts = line.split()
            delta_value = int(parts[2])  # 获取'delta'后的值
            deltas.append(delta_value)

# 计算平均delta
average_delta = sum(deltas) / len(deltas) if deltas else 0
print(f"1 平均delta值: {average_delta}")
with open('tmp2', 'r') as file:
    deltas = []
    for line in file:
        # 查找包含'delta'的行并提取其数值
        if 'delta' in line:
            parts = line.split()
            delta_value = int(parts[2])  # 获取'delta'后的值
            deltas.append(delta_value)

# 计算平均delta
average_delta = sum(deltas) / len(deltas) if deltas else 0
print(f"2 平均delta值: {average_delta}")
