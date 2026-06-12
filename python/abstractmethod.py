from abc import ABC, abstractmethod

class Shape(ABC):
    """抽象基类"""
    
    @abstractmethod
    def area(self):
        """计算面积（必须实现）"""
        pass
    
    @abstractmethod
    def perimeter(self):
        """计算周长（必须实现）"""
        pass
    
    # 非抽象方法（可选实现）
    def description(self):
        return f"This is a {self.__class__.__name__}"

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2
    
    def perimeter(self):
        return 2 * 3.14159 * self.radius

# 使用
# shape = Shape()  # TypeError: Can't instantiate abstract class

rect = Rectangle(5, 3)
print(rect.area())        # 15
print(rect.perimeter())   # 16
print(rect.description()) # This is a Rectangle