from dataclasses import dataclass, field
from typing import List

# 基础用法
@dataclass
class Person:
    name: str
    age: int
    email: str = ""  # 默认值

# 高级用法
@dataclass
class Employee:
    name: str
    salary: float
    department: str = "General"
    skills: List[str] = field(default_factory=list)  # 可变默认值
    id: int = field(init=False)  # 不在 __init__ 中
    
    def __post_init__(self):
        """初始化后处理"""
        self.id = hash(self.name) % 10000
    
    def give_raise(self, percent):
        self.salary *= (1 + percent / 100)

# 使用
emp1 = Employee("Alice", 50000, "Engineering", ["Python", "Java"])
emp2 = Employee("Bob", 60000)  # 使用默认值

print(emp1)  # Employee(name='Alice', salary=50000, department='Engineering', skills=['Python', 'Java'], id=...)
print(emp1 == emp2)  # False（自动生成 __eq__）

emp1.give_raise(10)
print(emp1.salary)  # 55000.0