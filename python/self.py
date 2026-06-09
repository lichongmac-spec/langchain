class Car:
    def __init__(self, brand):
        self.brand = brand  # self 指向实例本身
    
    def drive(self):
        print(f"{self.brand} is driving")

# 两种调用方式等价
car = Car("Toyota")
car.drive()           # Toyota is driving
Car.drive(car)        # 等价写法