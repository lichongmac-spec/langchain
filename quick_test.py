print("测试开始")
import sys
print(f"Python: {sys.version}")

try:
    import langchain_deepseek
    print("langchain_deepseek: OK")
except Exception as e:
    print(f"langchain_deepseek: ERROR - {e}")

try:
    from langchain_core.prompts import ChatPromptTemplate
    print("ChatPromptTemplate: OK")
except Exception as e:
    print(f"ChatPromptTemplate: ERROR - {e}")

try:
    from dotenv import load_dotenv
    import os
    load_dotenv()
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if api_key:
        print(f"API Key: {api_key[:10]}...")
    else:
        print("API Key: NOT FOUND")
except Exception as e:
    print(f"Env loading: ERROR - {e}")

print("测试完成")
