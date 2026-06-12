class JsonMixin:
    """提供JSON序列化能力"""
    def to_json(self):
        import json
        return json.dumps(self.__dict__)
    
    def from_json(cls, json_str):
        import json
        data = json.loads(json_str)
        return cls(**data)

class XmlMixin:
    """提供XML序列化能力（示例）"""
    def to_xml(self):
        items = [f"<{k}>{v}</{k}>" for k, v in self.__dict__.items()]
        return f"<{self.__class__.__name__}>{''.join(items)}</{self.__class__.__name__}>"

class User(JsonMixin, XmlMixin):
    def __init__(self, name, age):
        self.name = name
        self.age = age

user = User("Alice", 30)
print(user.to_json())  # {"name": "Alice", "age": 30}
print(user.to_xml())   # <User><name>Alice</name><age>30</age></User>