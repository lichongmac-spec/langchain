# 传统写法（其他语言）
# temp = a
# a = b
# b = temp

# Python写法
# a, b = b, a

a = 10
b = 20

# a, b = b, a 的执行步骤：
# 1. Python先计算右边的值：b=20, a=10 → 得到元组 (20, 10)
# 2. 再把元组解包赋值给左边：(a, b) = (20, 10)
# 3. 结果：a=20, b=10

print(a, b)  # 10 20

a, b = b, a
print(a, b)  #  20 10

# 1. 交换三个变量
x, y, z = 1, 2, 3
x, y, z = z, x, y
print(x, y, z)  # 3, 1, 2

# 2. 交换列表中的两个位置（需要索引）
arr = [1, 2, 3, 4]
arr[0], arr[2] = arr[2], arr[0]
print(arr)  # [3, 2, 1, 4]

# 3. 交换字典的值
data = {"name": "Alice", "age": 30}
data["name"], data["age"] = data["age"], data["name"]
print(data)  # {'name': 30, 'age': 'Alice'}

# *rest 会捕获所有剩余的元素（以列表形式）
*rest, last = [1, 2, 3, 4]
print(rest)  # [1, 2, 3]
print(last)  # 4

# 执行过程：
# 1. 右边列表有4个元素
# 2. last 匹配最后一个元素：4
# 3. *rest 匹配剩下的所有元素：[1, 2, 3]

# 1. 星号在开头：取第一个，剩下的给星号
first, *rest = [1, 2, 3, 4]
print(first)  # 1
print(rest)   # [2, 3, 4]

# 2. 星号在中间：取第一个和最后一个，中间给星号
first, *middle, last = [1, 2, 3, 4, 5]
print(first)   # 1
print(middle)  # [2, 3, 4]
print(last)    # 5

# 3. 多个星号？不行！只能有一个星号
# a, *b, *c = [1,2,3,4]  # SyntaxError

# 取第一个和最后一个
scores = [85, 92, 78, 90, 88]
first, *middle, last = scores
print(f"第一个: {first}")    # 85
print(f"中间: {middle}")     # [92, 78, 90]
print(f"最后一个: {last}")   # 88

# 如果只有2个元素
scores = [85, 88]
first, *middle, last = scores
print(first)   # 85
print(middle)  # []
print(last)    # 88

def get_user_info():
    return "Alice", 30, "alice@example.com", "北京"

# 只取前两个和最后一个
name, age, *rest, city = get_user_info()
print(name)   # Alice
print(age)    # 30
print(rest)   # ['alice@example.com']
print(city)   # 北京

# 1. 星号在开头：取第一个，剩下的给星号
first, *rest = [1, 2, 3, 4]
print(first)  # 1
print(rest)   # [2, 3, 4]

# 2. 星号在中间：取第一个和最后一个，中间给星号
first, *middle, last = [1, 2, 3, 4, 5]
print(first)   # 1
print(middle)  # [2, 3, 4]
print(last)    # 5

# 3. 多个星号？不行！只能有一个星号
# a, *b, *c = [1,2,3,4]  # SyntaxError

# 取第一个和最后一个
scores = [85, 92, 78, 90, 88]
first, *middle, last = scores
print(f"第一个: {first}")    # 85
print(f"中间: {middle}")     # [92, 78, 90]
print(f"最后一个: {last}")   # 88

# 如果只有2个元素
scores = [85, 88]
first, *middle, last = scores
print(first)   # 85
print(middle)  # []
print(last)    # 88

def get_user_info():
    return "Alice", 30, "alice@example.com", "北京"

# 只取前两个和最后一个
name, age, *rest, city = get_user_info()
print(name)   # Alice
print(age)    # 30
print(rest)   # ['alice@example.com']
print(city)   # 北京

log_line = "2024-01-15 10:30:45 ERROR Database connection failed"

date, time, level, *messages = log_line.split()
print(date)      # 2024-01-15
print(time)      # 10:30:45
print(level)     # ERROR
print(messages)  # ['Database', 'connection', 'failed']
print(' '.join(messages))  # Database connection failed

# 使用 _ 表示不需要的值
_, second, *_, last = [1, 2, 3, 4, 5]
print(second)  # 2
print(last)    # 5

# 或者明确忽略中间部分
first, *_, last = [10, 20, 30, 40, 50]
print(first)   # 10
print(last)    # 50

# 元组和列表一样支持
point = (10, 20)
x, y = point
print(x, y)  # 10 20

# 元组的星号
numbers = (1, 2, 3, 4, 5)
first, *rest = numbers
print(first)  # 1
print(rest)   # [2, 3, 4, 5]  # 注意：结果变成了列表

# 字符串也可以解包
a, b, c = "ABC"
print(a, b, c)  # A B C

# 星号用于字符串
first, *middle, last = "Hello"
print(first)   # H
print(middle)  # ['e', 'l', 'l']
print(last)    # o

# 合并字符串
words = ["Hello", "World"]
result = " ".join(words)  # Hello World
print(result)  # Hello World

# 字典解包得到的是键
d = {"name": "Alice", "age": 30}
a, b = d
print(a, b)  # name age

# 获取键和值
for key, value in d.items():
    print(f"{key}: {value}")

# 合并字典（3.9+）
d1 = {"a": 1, "b": 2}
d2 = {"c": 3, "d": 4}
merged = {**d1, **d2}
print(merged)  # {'a': 1, 'b': 2, 'c': 3, 'd': 4}

print('场景1：实现队列的pop操作')

class Queue:
    def __init__(self, items):
        self.items = items
    
    def pop_front(self):
        first, *self.items = self.items
        return first

q = Queue([1, 2, 3, 4])
print(q.pop_front())  # 1
print(q.items)        # [2, 3, 4]

print('场景2：分组处理数据')
# 将数据分成头和尾
def process_data(data):
    if not data:
        return None, []
    
    head, *tail = data
    return head, tail

result = process_data([1, 2, 3, 4])
print(result)  # (1, [2, 3, 4])

print('场景3：递归函数')
# 计算列表和（递归版）
def sum_list(numbers):
    if not numbers:
        return 0
    first, *rest = numbers
    return first + sum_list(rest)

print(sum_list([1, 2, 3, 4, 5]))  # 15

print('场景4：提取关键信息')
# 解析CSV行
csv_line = "Alice,30,Engineer,alice@example.com,USA"
name, age, *rest, country = csv_line.split(',')

print(f"姓名: {name}")
print(f"年龄: {age}")
print(f"其他: {rest}")      # ['Engineer', 'alice@example.com']
print(f"国家: {country}")   # USA

print('技巧1：嵌套解包')

# 解包嵌套结构
data = [(1, 2), (3, 4), (5, 6)]
for a, b in data:
    print(f"{a} + {b} = {a+b}")

# 复杂嵌套
person = ("Alice", 30, ["Python", "Java"], {"city": "北京"})
name, age, [first_lang, second_lang], address = person
print(name, age, first_lang, second_lang, address)

print('技巧2：函数参数中的星号')
# *args 收集多余的位置参数
def func(a, b, *args):
    print(f"a={a}, b={b}, 其他={args}")

func(1, 2, 3, 4, 5)  # a=1, b=2, 其他=(3, 4, 5)

# **kwargs 收集多余的关键字参数
def func2(a, b, **kwargs):
    print(f"a={a}, b={b}, 其他={kwargs}")

func2(1, 2, x=10, y=20)  # a=1, b=2, 其他={'x': 10, 'y': 20}


print("技巧3：展开列表/元组")
# 使用 * 展开列表
numbers = [1, 2, 3]
print([0, *numbers, 4])  # [0, 1, 2, 3, 4]

# 函数调用时展开
def add(a, b, c):
    return a + b + c

nums = [10, 20, 30]
print(add(*nums))  # 60

# 合并列表
list1 = [1, 2]
list2 = [3, 4]
merged = [*list1, *list2]
print(merged)  # [1, 2, 3, 4]

print('题1：变量交换')
# 不使用临时变量，交换以下变量的值
x = "Hello"
y = "World"
z = "Python"

# 你的代码
x, y, z = z, x, y
print(x, y, z)  # Python Hello World

print("题2：提取数据")

# 从列表中提取第一个、第三个和最后一个元素
data = [100, 200, 300, 400, 500, 600]

# 你的代码
first, _, third, *_, last = data
print(first, third, last)  # 100 300 600

print('题3：实现split方法')

# 实现一个函数，将字符串按分隔符分割成头和尾两部分
def split_first_rest(text, sep=' '):
    # 你的代码
    parts = text.split(sep)
    if not parts:
        return None, []
    first, *rest = parts
    return first, rest

print(split_first_rest("apple banana cherry"))
# ('apple', ['banana', 'cherry'])