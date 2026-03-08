from langchain_deepseek import ChatDeepSeek
import inspect

# 检查 ChatDeepSeek 类的签名
print("ChatDeepSeek 构造函数签名:")
signature = inspect.signature(ChatDeepSeek.__init__)
print(signature)

# 检查 ChatDeepSeek 类的文档
print("\nChatDeepSeek 文档:")
print(ChatDeepSeek.__doc__)

# 检查基类
print("\nChatDeepSeek 基类:")
print(ChatDeepSeek.__bases__)

# 检查类属性
print("\nChatDeepSeek 类属性:")
for attr in dir(ChatDeepSeek):
    if not attr.startswith('_'):
        print(f"  {attr}")
