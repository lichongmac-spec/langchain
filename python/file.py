print('文件与异常处理')
# 1. 安全的文件读取（自动关闭）
try:
    with open('data.txt', 'r', encoding='utf-8') as f:
        content = f.read()
        lines = f.readlines()  # 逐行读
except FileNotFoundError as e:
    print(f"文件不存在: {e}")

# 2. 逐行写入文件
with open('output.txt', 'w') as f:
    for i in range(10):
        f.write(f"第{i}行\n")