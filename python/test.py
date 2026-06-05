# 1. 平方数
squares = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]

# 2. 字符串处理
names = ["alice", "bob", "charlie"]
capitalized = [name.title() for name in names]  # ['Alice', 'Bob', 'Charlie']

# 3. 嵌套循环（等价于笛卡尔积）
pairs = [(x,y) for x in [1,2] for y in ['a','b']]
# [(1,'a'), (1,'b'), (2,'a'), (2,'b')]

# 4. 条件 else 分支（注意：if-else 放在前面）
results = [x*2 if x%2==0 else x*3 for x in range(5)]
# x=0: 0*2=0
# x=1: 1*3=3
# x=2: 2*2=4
# x=3: 3*3=9
# x=4: 4*2=8
# 结果：[0, 3, 4, 9, 8]

# 5. 字典推导式（升级版）
squares_dict = {x: x**2 for x in range(5)}
# {0:0, 1:1, 2:4, 3:9, 4:16}

# 过滤出1-20中能被3整除的数字，并乘以10
# 期望结果：[30, 60, 90, 120, 150, 180]

# 你的答案：
result = [x*10 for x in range(1, 21) if x % 3 == 0]
print(result)  # [30, 60, 90, 120, 150, 180]

print('0==================')
squares=[x**2 for x in range(5)]
print(squares) #[0, 1, 4, 9, 16]

print('1====字符串处理==============')
names = ["alice","bob","charlie"]
capitalized = [name.title() for name in names]
print(capitalized) #['Alice', 'Bob', 'Charlie']


print('3. 嵌套循环（等价于笛卡尔积）')
pairs = [(x,y) for x in [1,2] for y in ['a','b']]
print(pairs) # [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]

print('4. 条件 else 分支（注意：if-else 放在前面）')
results=[x * 2 if x % 2 ==0 else x * 3 for x in range(5)]
print(results) # [0, 3, 4, 9, 8]

print('5. 字典推导式（升级版）')
squares_dict ={x : x**2 for x in range(5)}
print(squares_dict) # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

result=[x*10 for x in range(1,21) if x % 3 ==0]
print(result) # [30, 60, 90, 120, 150, 180]

