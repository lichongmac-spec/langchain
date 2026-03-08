from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv
import os

# 加载.env文件中的环境变量
load_dotenv()

# 获取API密钥
api_key = os.getenv("DEEPSEEK_API_KEY")
print(f"API Key: {api_key[:5]}...")

# 初始化模型
print("初始化模型...")
try:
    model = ChatDeepSeek(
        model="deepseek-chat",
        api_key=api_key,
        temperature=0.7,
    )
    print("模型初始化成功")
    
    # 测试基本调用
    print("\n测试基本调用...")
    response = model.invoke("Hello, how are you?")
    print(f"响应: {response.content}")
    
    # 测试带思考模式的调用
    print("\n测试带思考模式的调用...")
    response_with_thinking = model.invoke(
        "What is the capital of France?",
        extra_body={"thinking": {"type": "enabled", "budget_tokens": 5000}}
    )
    print(f"响应: {response_with_thinking.content}")
    print(f"additional_kwargs: {response_with_thinking.additional_kwargs}")
    
except Exception as e:
    print(f"错误: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("测试完成!")
