"""
LangChain 环境诊断脚本
检查 Python 环境和 LangChain 相关包的安装情况
"""

import sys
import os
from pathlib import Path

print("=" * 60)
print("LangChain 环境诊断")
print("=" * 60)

# 1. Python 版本
print(f"\n1. Python 版本: {sys.version}")
print(f"   Python 路径: {sys.executable}")

# 2. LangChain 相关包
print("\n2. LangChain 相关包:")
try:
    import importlib.metadata as metadata
    packages = [
        "langchain",
        "langchain-core",
        "langchain-openai",
        "langchain-deepseek",
        "langchain-anthropic",
        "langgraph",
        "python-dotenv",
    ]
    
    for pkg in packages:
        try:
            version = metadata.version(pkg)
            print(f"   ✓ {pkg}: {version}")
        except metadata.PackageNotFoundError:
            print(f"   ✗ {pkg}: 未安装")
except Exception as e:
    print(f"   错误: {e}")

# 3. 环境变量
print("\n3. 环境变量:")
env_vars = ["DEEPSEEK_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY"]
for var in env_vars:
    value = os.getenv(var)
    if value:
        print(f"   ✓ {var}: {value[:10]}... (已设置)")
    else:
        print(f"   ✗ {var}: 未设置")

# 4. .env 文件
print("\n4. .env 文件:")
env_paths = [
    Path.cwd() / ".env",
    Path.home() / ".env",
    Path(__file__).parent / ".env",
]
for path in env_paths:
    if path.exists():
        print(f"   ✓ 找到: {path}")
        try:
            with open(path, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                print(f"     包含 {len(lines)} 个环境变量")
        except Exception as e:
            print(f"     读取错误: {e}")
    else:
        print(f"   - 未找到: {path}")

# 5. 导入测试
print("\n5. 导入测试:")
modules_to_test = [
    ("langchain", "import langchain"),
    ("langchain_core", "from langchain_core.prompts import ChatPromptTemplate"),
    ("langchain_deepseek", "from langchain_deepseek import ChatDeepSeek"),
    ("langchain_openai", "from langchain_openai import ChatOpenAI"),
    ("langgraph", "from langgraph.graph import StateGraph"),
    ("dotenv", "from dotenv import load_dotenv"),
]

for name, import_stmt in modules_to_test:
    try:
        exec(import_stmt)
        print(f"   ✓ {name}: 导入成功")
    except Exception as e:
        print(f"   ✗ {name}: {type(e).__name__}: {e}")

# 6. 基本功能测试
print("\n6. 基本功能测试:")
try:
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_deepseek import ChatDeepSeek
    from dotenv import load_dotenv
    
    load_dotenv()
    
    # 测试提示模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个助手"),
        ("human", "{input}")
    ])
    print(f"   ✓ ChatPromptTemplate: 创建成功")
    
    # 测试模型初始化（不调用 API）
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if api_key:
        print(f"   ✓ DEEPSEEK_API_KEY: 已设置")
        try:
            model = ChatDeepSeek(
                model="deepseek-chat",
                api_key=api_key,
                temperature=0.7
            )
            print(f"   ✓ ChatDeepSeek: 初始化成功")
        except Exception as e:
            print(f"   ✗ ChatDeepSeek 初始化失败: {type(e).__name__}: {e}")
    else:
        print(f"   ✗ DEEPSEEK_API_KEY: 未设置，无法测试模型")
    
except Exception as e:
    print(f"   ✗ 功能测试失败: {type(e).__name__}: {e}")

# 7. 常见问题检查
print("\n7. 常见问题检查:")

# 检查 Python 路径
if "site-packages" in sys.executable.lower():
    print(f"   ✓ 使用系统 Python: {sys.executable}")
else:
    print(f"   ! 使用虚拟环境: {sys.executable}")

# 检查 pip 版本
try:
    import pip
    print(f"   ✓ pip 版本: {pip.__version__}")
except:
    print(f"   ! 无法获取 pip 版本")

print("\n" + "=" * 60)
print("诊断完成")
print("=" * 60)

# 8. 建议
print("\n建议:")
print("1. 确保所有 LangChain 相关包版本兼容")
print("2. 检查 .env 文件是否正确配置")
print("3. 确保使用虚拟环境而不是系统 Python")
print("4. 如果遇到导入错误，尝试重新安装相关包")
print("5. 检查网络连接和 API 密钥是否有效")
