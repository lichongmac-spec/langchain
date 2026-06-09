# 类 - 蓝图/模板
class Dog:
    """这是一个狗类"""
    
    # 类属性（所有实例共享）
    species = "Canis familiaris"
    
    # 实例属性（每个实例独有）
    def __init__(self, name, age):
        self.name = name      # 实例属性
        self.age = age        # 实例属性
    
    # 实例方法
    def bark(self):
        return f"{self.name} says Woof!"
    
    # 特殊方法（字符串表示）
    def __str__(self):
        return f"{self.name} ({self.age} years old)"

# 创建对象（实例化）
my_dog = Dog("Buddy", 3)
print(my_dog)          # Buddy (3 years old)
print(my_dog.bark())   # Buddy says Woof!
print(my_dog.species)  # Canis familiaris