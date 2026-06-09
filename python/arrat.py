class Employee:
    # 类属性（所有实例共享）
    company = "Every Inc"
    raise_amount = 1.05
    
    def __init__(self, name, salary):
        # 实例属性（每个实例独有）
        self.name = name
        self.salary = salary
    
    def apply_raise(self):
        self.salary = int(self.salary * self.raise_amount)

# 使用
emp1 = Employee("Alice", 50000)
emp2 = Employee("Bob", 60000)

print(emp1.company)  # Every Inc
print(emp2.company)  # Every Inc

# 修改类属性会影响所有实例
Employee.company = "Every Technologies"
print(emp1.company)  # Every Technologies

# 修改实例属性不影响其他实例
emp1.raise_amount = 1.10
print(emp1.raise_amount)  # 1.10
print(emp2.raise_amount)  # 1.05