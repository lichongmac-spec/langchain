"""
LangChain 详细测试脚本
"""

import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek

print("=" * 60)
print("LangChain 详细测试")
print("=" * 60)

# 1. 加载环境变量
print("\n1. 加载环境变量...")
load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
if api_key:
    print(f"   ✓ DEEPSEEK_API_KEY: {api_key[:10]}...")
else:
    print("   ✗ DEEPSEEK_API_KEY: 未设置")
    exit(1)

# 2. 创建提示模板
print("\n2. 创建提示模板...")
try:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个专业的翻译"),
        ("human", "{input}")
    ])
    print("   ✓ 提示模板创建成功")
except Exception as e:
    print(f"   ✗ 提示模板创建失败: {e}")
    exit(1)

# 3. 初始化模型
print("\n3. 初始化模型...")
try:
    llm = ChatDeepSeek(
        model="deepseek-chat",
        api_key=api_key,
        temperature=0.7
    )
    print("   ✓ 模型初始化成功")
except Exception as e:
    print(f"   ✗ 模型初始化失败: {e}")
    exit(1)

# 4. 创建链
print("\n4. 创建链...")
try:
    chain = prompt | llm
    print("   ✓ 链创建成功")
except Exception as e:
    print(f"   ✗ 链创建失败: {e}")
    exit(1)

# 5. 测试调用
print("\n5. 测试调用...")
try:
    print("   正在调用模型...")
    response = chain.invoke({"input": "你好"})
    print(f"   ✓ 调用成功")
    print(f"\n响应内容:")
    print(f"   {response.content}")
except Exception as e:
    print(f"   ✗ 调用失败: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
