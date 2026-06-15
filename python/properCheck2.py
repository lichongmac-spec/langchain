class Product:
    """产品类"""
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
    
    @property
    def total_value(self):
        """计算总价值（只读）"""
        pass
    
    @price.setter
    def price(self, value):
        """价格必须 > 0"""
        pass
    
    @quantity.setter
    def quantity(self, value):
        """数量 >= 0"""
        pass