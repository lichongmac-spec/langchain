# 先创建文件并写入内容
with open('data.txt', 'w', encoding='utf-8') as f:
    f.write('这是第一行\n')
    f.write('这是第二行\n')
    f.write('这是第三行')


# 读取整个文件
with open('data.txt', 'r', encoding='utf-8') as f:
    content = f.read()
    print(content)

# 逐行读取（推荐大文件）
with open('data.txt', 'r', encoding='utf-8') as f:
    for line in f:
        print(line.strip())  # strip()去掉换行符

# 读取所有行到列表
with open('data.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    print(lines)  # ['第一行\n', '第二行\n', '第三行']

# 追加写入
with open('data.txt', 'a', encoding='utf-8') as f:
    f.write('\n这是追加的内容')

# 写入多行
lines = ['行1', '行2', '行3']
with open('output.txt', 'w', encoding='utf-8') as f:
    f.writelines([line + '\n' for line in lines])