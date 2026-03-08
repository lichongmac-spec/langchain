"""
简单的 LangChain 环境检查
"""

import sys
print(f"Python 版本: {sys.version}")
print(f"Python 路径: {sys.executable}")

# 检查包
packages = ["langchain", "langchain-core", "langchain-deepseek", "langchain-openai"]
for pkg in packages:
    try:
        __import__(pkg.replace("-", "_"))
        print(f"✓ {pkg}: 已安装")
    except ImportError:
        print(f"✗ {pkg}: 未安装")

# 检查环境变量
import os
api_key = os.getenv("DEEPSEEK_API_KEY")
if api_key:
    print(f"✓ DEEPSEEK_API_KEY: 已设置")
else:
    print(f"✗ DEEPSEEK_API_KEY: 未设置")

# 测试导入
print("\n测试导入:")
try:
    from langchain_core.prompts import ChatPromptTemplate
    print("✓ ChatPromptTemplate 导入成功")
except Exception as e:
    print(f"✗ ChatPromptTemplate 导入失败: {e}")

try:
    from langchain_deepseek import ChatDeepSeek
    print("✓ ChatDeepSeek 导入成功")
except Exception as e:
    print(f"✗ ChatDeepSeek 导入失败: {e}")
