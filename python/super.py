class Person:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def info(self):
        return f"Person: {self.name} <{self.email}>"

class Student(Person):
    def __init__(self, name, email, student_id):
        super().__init__(name, email)  # 调用父类初始化
        self.student_id = student_id
    
    def info(self):
        # 扩展父类方法
        base_info = super().info()
        return f"{base_info}, Student ID: {self.student_id}"

# 使用
student = Student("Alice", "alice@example.com", "S12345")
print(student.info())  # Person: Alice <alice@example.com>, Student ID: S12345