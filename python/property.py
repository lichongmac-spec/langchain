class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius
    
    # getter
    @property
    def celsius(self):
        return self._celsius
    
    # setter
    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("温度不能低于绝对零度")
        self._celsius = value
    
    # deleter
    @celsius.deleter
    def celsius(self):
        print("删除温度")
        del self._celsius
    
    # 计算属性
    @property
    def fahrenheit(self):
        return self._celsius * 9/5 + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5/9

# 使用
temp = Temperature(25)
print(temp.celsius)        # 25（像属性一样访问）
temp.celsius = 30          # 调用setter
print(temp.fahrenheit)     # 86.0

temp.fahrenheit = 100
print(temp.celsius)        # 37.777...

# del temp.celsius         # 调用deleter

print('使用 property 实现只读属性')
class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        return self._radius
    
    @property
    def area(self):
        return 3.14159 * self._radius ** 2
    
    @property
    def diameter(self):
        return self._radius * 2

circle = Circle(5)
print(circle.radius)    # 5
print(circle.area)      # 78.53975
# circle.radius = 10    # AttributeError（没有setter）