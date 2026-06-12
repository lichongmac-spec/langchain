class Flyable:
    def fly(self):
        return "Flying..."
    
    def move(self):
        return "Flying through air"

class Swimmable:
    def swim(self):
        return "Swimming..."
    
    def move(self):
        return "Swimming in water"

class Duck(Flyable, Swimmable):
    def __init__(self, name):
        self.name = name
    
    def move(self):
        # 选择调用哪个父类的方法
        return f"{self.name} can both {Flyable.move(self)} and {Swimmable.move(self)}"
    
    def speak(self):
        return "Quack!"

# 方法解析顺序（MRO）
duck = Duck("Donald")
print(duck.fly())           # Flying...
print(duck.swim())          # Swimming...
print(duck.move())          # Donald can both Flying through air and Swimming in water
print(Duck.__mro__)         # (Duck, Flyable, Swimmable, object)