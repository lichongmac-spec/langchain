# 复制到文件中运行，看看是否都能正常输出
print("=== Python复习验收 ===")

# 1. 列表推导式
assert [x*2 for x in range(5)] == [0,2,4,6,8]

# 2. 解包
a,b = 1,2
a,b = b,a
assert a==2 and b==1

# 3. with语句
with open("/tmp/test.txt", "w") as f:
    f.write("hello")
    
# 4. 装饰器
def timer(func):
    def wrapper(*args):
        return func(*args)
    return wrapper

@timer
def hello():
    return "world"

# 5. 导入外部库
import requests
print("所有检查通过！")