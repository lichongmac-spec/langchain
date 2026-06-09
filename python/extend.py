class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        raise NotImplementedError("子类必须实现此方法")
    
    def move(self):
        return f"{self.name} is moving"

class Dog(Animal):
    def speak(self):
        return f"{self.name} says Woof!"
    
    # 添加新方法
    def wag_tail(self):
        return f"{self.name} is wagging tail"

class Cat(Animal):
    def speak(self):
        return f"{self.name} says Meow!"
    
    def purr(self):
        return f"{self.name} is purring"

# 使用
dog = Dog("Buddy")
cat = Cat("Kitty")

print(dog.speak())   # Buddy says Woof!
print(cat.speak())   # Kitty says Meow!
print(dog.move())    # Buddy is moving
print(dog.wag_tail()) # Buddy is wagging tail