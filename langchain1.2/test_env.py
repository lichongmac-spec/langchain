from dotenv import load_dotenv
import os

# 加载.env文件中的环境变量
print("加载.env文件...")
load_dotenv()

# 获取API密钥
api_key = os.getenv("DEEPSEEK_API_KEY")
print(f"API Key: {api_key}")

# 测试基本打印
print("测试基本打印功能...")
print("Hello, World!")
print("测试完成!")
