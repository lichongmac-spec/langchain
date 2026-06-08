# 生成器是一种特殊的迭代器，使用 yield 关键字可以逐个产生值，而不是一次性返回所有结果。
# 核心优势：省内存！ 适合处理大量数据或无限序列。
def count_up_to(n):
    """逐条产出从1到n的数字"""
    i = 1
    while i <= n:
        print(f"准备产出 {i}")  # 观察执行过程
        yield i                 # 产出值，暂停函数
        print(f"{i} 已产出，继续")
        i += 1

# 创建生成器对象
gen = count_up_to(3)
print(gen)  # <generator object count_up_to at 0x...>

# 逐条获取值
print(next(gen))  # 准备产出 1 → 1
print(next(gen))  # 1 已产出，继续 → 准备产出 2 → 2
print(next(gen))  # 2 已产出，继续 → 准备产出 3 → 3
# print(next(gen))  # StopIteration 异常

print('===for循环自动调用')

def count_up_to(n):
    i = 1
    while i <= n:
        yield i
        i += 1

# for循环自动处理 StopIteration
for num in count_up_to(5):
    print(num, end=' ')  # 1 2 3 4 5

print('普通函数：一次性返回所有数据')

def get_numbers_list(n):
    """返回列表（占用大量内存）"""
    result = []
    for i in range(n):
        result.append(i)
    return result

# 内存占用：100万个整数 → 约28MB
numbers = get_numbers_list(1_000_000)
print(f"列表大小: {len(numbers)}")


print('生成器：逐个产出数据')

def get_numbers_generator(n):
    """生成器（几乎不占内存）"""
    for i in range(n):
        yield i

# 内存占用：几乎为0
gen = get_numbers_generator(1_000_000)
print(f"生成器对象: {gen}")
# 使用时才逐个产生
for i in gen:
    if i > 10:
        break  # 可以提前停止
    print(i, end=' ')

print('实际内存对比')
import sys

def list_version(n):
    return [i for i in range(n)]

def generator_version(n):
    for i in range(n):
        yield i

n = 100_000
list_data = list_version(n)
gen_data = generator_version(n)

print(f"列表内存: {sys.getsizeof(list_data):,} 字节")  # 约800KB
print(f"生成器内存: {sys.getsizeof(gen_data):,} 字节")  # 约112字节
# 差距巨大！生成器内存占用恒定