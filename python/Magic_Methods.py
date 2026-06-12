class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    # 字符串表示
    def __str__(self):
        return f"Vector({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Vector(x={self.x}, y={self.y})"
    
    # 算术运算
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
    
    # 比较运算
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __lt__(self, other):
        return (self.x**2 + self.y**2) < (other.x**2 + other.y**2)
    
    # 长度
    def __len__(self):
        return 2
    
    # 索引访问
    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        raise IndexError("Index out of range")
    
    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError("Index out of range")
    
    # 迭代器
    def __iter__(self):
        yield self.x
        yield self.y
    
    # 调用对象
    def __call__(self, factor):
        return Vector(self.x * factor, self.y * factor)

# 使用
v1 = Vector(2, 3)
v2 = Vector(4, 5)

print(v1)                    # Vector(2, 3)  (__str__)
print(repr(v1))              # Vector(x=2, y=3)  (__repr__)

v3 = v1 + v2                 # __add__
print(v3)                    # Vector(6, 8)

print(v1 == v2)              # False (__eq__)
print(v1 < v2)               # True (__lt__)

print(len(v1))               # 2 (__len__)
print(v1[0])                 # 2 (__getitem__)
v1[1] = 10                   # __setitem__
print(v1)                    # Vector(2, 10)

for comp in v1:              # __iter__
    print(comp)              # 2, 10

v4 = v1(2)                   # __call__
print(v4)                    # Vector(4, 20)