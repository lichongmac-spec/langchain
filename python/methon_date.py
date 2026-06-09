class Date:
    """日期类演示三种方法的用途"""
    
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
    
    # 实例方法：处理实例数据
    def format(self):
        return f"{self.year}-{self.month:02d}-{self.day:02d}"
    
    # 类方法：替代构造函数
    @classmethod
    def from_string(cls, date_str):
        """从字符串创建日期对象"""
        year, month, day = map(int, date_str.split('-'))
        return cls(year, month, day)
    
    # 类方法：获取类级别信息
    @classmethod
    def today(cls):
        """获取今天日期"""
        from datetime import date
        today = date.today()
        return cls(today.year, today.month, today.day)
    
    # 静态方法：工具函数，与类相关但不依赖实例
    @staticmethod
    def is_valid(year, month, day):
        """验证日期是否有效"""
        if month < 1 or month > 12:
            return False
        if day < 1 or day > 31:
            return False
        return True

# 使用
date1 = Date(2024, 12, 25)
print(date1.format())          # 2024-12-25

date2 = Date.from_string("2024-01-15")
print(date2.format())          # 2024-01-15

date3 = Date.today()
print(date3.format())          # 今天日期

print(Date.is_valid(2024, 13, 1))   # False