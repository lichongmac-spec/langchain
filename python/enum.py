from enum import Enum, auto, unique

@unique  # 确保值唯一
class Status(Enum):
    PENDING = 1
    PROCESSING = 2
    COMPLETED = 3
    FAILED = 4

class Color(Enum):
    RED = auto()   # 自动赋值 1
    GREEN = auto() # 2
    BLUE = auto()  # 3

# 使用
status = Status.PENDING
print(status)          # Status.PENDING
print(status.name)     # PENDING
print(status.value)    # 1

# 比较
print(status == Status.PENDING)  # True
print(status is Status.PENDING)  # True

# 遍历
for status in Status:
    print(f"{status.name}: {status.value}")

# 通过值获取
status = Status(1)
print(status)  # Status.PENDING