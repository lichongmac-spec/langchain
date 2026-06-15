class BankAccount:
    """实现银行账户类"""
    # 类属性：利率
    interest_rate = 0.02
    
    def __init__(self, account_number, balance=0):
        self.account_number = account_number
        self._balance = balance
    
    @property
    def balance(self):
        return self._balance
    
    def deposit(self, amount):
        # 存入金额
        pass
    
    def withdraw(self, amount):
        # 取款（不能透支）
        pass
    
    def add_interest(self):
        # 添加利息
        pass
    
    def __str__(self):
        return f"Account {self.account_number}: ${self.balance:.2f}"

# 测试
acc = BankAccount("12345", 1000)
acc.deposit(500)
acc.withdraw(200)
acc.add_interest()
print(acc)  # Account 12345: $1326.00