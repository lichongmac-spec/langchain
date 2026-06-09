class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner           # 公有属性
        self._password = "1234"      # 保护属性（约定：不要直接访问）
        self.__balance = balance     # 私有属性（名称修饰）
    
    def get_balance(self):           # 公有方法访问私有属性
        return self.__balance
    
    def _internal_method(self):      # 保护方法
        pass
    
    def __private_method(self):      # 私有方法
        pass

account = BankAccount("Alice", 1000)
print(account.owner)           # Alice
print(account._password)       # 可以访问但不建议
# print(account.__balance)     # AttributeError
print(account.get_balance())   # 1000

# 名称修饰：实际存储为 _BankAccount__balance
print(account._BankAccount__balance)  # 1000（不建议这样做）