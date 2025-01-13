import pandas as pd
import re

# 读取 time_diff.csv 文件，并存储为字典，优化查找速度
def load_time_diff(file_path):
    time_diff_df = pd.read_csv(file_path)
    time_diff_dict = {}
    
    # 只存储整数部分时间戳和对应的 diff
    for _, row in time_diff_df.iterrows():
        timestamp = str(row['timestamp']).split('.')[0]  # 只取整数部分
        time_diff_dict[timestamp] = row['diff']
    
    return time_diff_dict

# 打开 log 文件并读取所有行
log_file_path = "logs.txt"
with open(log_file_path, "r") as file:
    log_lines = file.readlines()

# 用来存储匹配的数据
matching_data = []

# 加载 time_diff 字典
time_diff_dict = load_time_diff("time_diff.csv")

# 正则表达式，用于提取日志中的信息
log_pattern = re.compile(r"(?P<timestamp>\d+\.\d+)\s+ptp4l\[\d+\.\d+\]:\s+master offset\s+(?P<master_offset>-?\d+)\s+s2\s+freq\s+(?P<freq>-?\d+)\s+path delay\s+(?P<path_delay>\d+)")

# 遍历日志文件中的每一行，提取数据
for line in log_lines:
    match = log_pattern.search(line)
    if match:
        timestamp = match.group("timestamp").split('.')[0]  # 只保留整数部分的时间戳
        master_offset = int(match.group("master_offset"))
        freq = int(match.group("freq"))
        path_delay = int(match.group("path_delay"))
        
        # 从 time_diff 字典中查找对应的 diff
        if timestamp in time_diff_dict:
            diff = time_diff_dict[timestamp]
            matching_data.append([timestamp, diff, master_offset, freq, path_delay])

output_df = pd.DataFrame(matching_data, columns=["time", "target", "master_offset", "freq", "path_delay"])
output_df.to_csv("matched_data.csv", index=False)

# 打印结果查看
print(output_df)
