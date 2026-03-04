from langchain.chains import LLMMathChain
from langchain_openai import ChatOpenAI, OpenAI
import os
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

# 获取API密钥
minimax_api_key = os.getenv("MINIMAX_API_KEY")

# 确保API密钥存在
if not minimax_api_key:
    raise ValueError("MINIMAX_API_KEY 必须在.env文件中设置")

llm = ChatOpenAI(
    model=os.getenv("MINIMAX_MODEL_NAME", "MiniMax-M2.5"),  # 或 "deepseek-reasoner"
    openai_api_key=minimax_api_key,
    openai_api_base="https://api.minimax.chat/v1",
    temperature=0.7,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# 调用模型并打印响应
response = llm.invoke('你好')
print("模型响应:", response)