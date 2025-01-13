import pandas as pd

# 读取文件 'times.txt'
with open("times.txt", "r") as file:
    lines = file.readlines()

# 存储 server#0 和 server#1 的时间戳
timestamps_0 = []
timestamps_1 = []

# 解析文件中的每一行，提取时间戳
for line in lines:
    server, timestamp = line.strip().split(": ")
    if "server#0" in server:
        timestamps_0.append(float(timestamp))
    elif "server#1" in server:
        timestamps_1.append(float(timestamp))

# 计算相邻的时间戳差值
data = []
for t0, t1 in zip(timestamps_0, timestamps_1):
    timestamp = t0  # 使用 server#0 的时间戳作为基准时间
    time_diff = t1 - t0  # 计算差值
    data.append([timestamp, time_diff])

# 将数据保存为 CSV 文件
df = pd.DataFrame(data, columns=["timestamp", "diff"])
df.to_csv("time_diff.csv", index=False)

# 打印结果查看
print(df)
