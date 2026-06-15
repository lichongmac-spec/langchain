class Database:
    def __init__(self):
        self._connection = None
    
    @property
    def connection(self):
        if self._connection is None:
            print("Creating database connection...")
            self._connection = "Fake Connection"
        return self._connection

db = Database()
print(db.connection)  # 创建连接
print(db.connection)  # 直接返回