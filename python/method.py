class MyClass:
    class_var = 0
    
    def __init__(self, value):
        self.value = value
    
    # 实例方法（需要 self，可访问实例属性和类属性）
    def instance_method(self):
        return f"实例方法: value={self.value}, class_var={self.class_var}"
    
    # 类方法（需要 cls，只能访问类属性）
    @classmethod
    def class_method(cls):
        cls.class_var += 1
        return f"类方法: class_var={cls.class_var}"
    
    # 静态方法（不需要 self/cls，独立函数）
    @staticmethod
    def static_method(x, y):
        return f"静态方法: {x + y}"

# 使用
obj = MyClass(10)

# 实例方法（必须通过实例调用）
print(obj.instance_method())

# 类方法（可通过类或实例调用）
print(MyClass.class_method())  # 类方法: class_var=1
print(obj.class_method())      # 类方法: class_var=2

# 静态方法
print(MyClass.static_method(3, 5))  # 静态方法: 8
print(obj.static_method(4, 6))      # 静态方法: 10