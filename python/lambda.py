print('函数式编程')
# 1. 用lambda和filter筛选出偶数
nums = [1,2,3,4,5,6]
evens = list(filter(lambda x: x%2==0, nums))
print(evens)



# 2. 用map和lambda把字符串列表转成int
str_nums = ["1","2","3"]
ints = list(map(int, str_nums))
print(ints)
# 3. 用reduce计算阶乘
from functools import reduce
factorial_5 = reduce(lambda x,y: x*y, range(1,6))
print(factorial_5)
# 120
