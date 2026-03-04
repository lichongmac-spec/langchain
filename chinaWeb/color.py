import os
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import BaseOutputParser

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 设置项目根目录（color.py 所在目录的父目录）
project_root = os.path.abspath(os.path.join(current_dir, ".."))
# 将根目录添加到系统路径
sys.path.insert(0, project_root)

# 加载.env文件（从项目根目录）
load_dotenv(dotenv_path=os.path.join(project_root, ".env"))

class CommaSeparatedListOutputParser(BaseOutputParser):
    """Parse the output of an LLM call to a comma-separated list."""

    def parse(self, text: str):
        """Parse the output of an LLM call."""
        # 移除 <think> 标签和内容
        if "<think>" in text and "</think>" in text:
            text = text.split("</think>")[1].strip()
        return text.strip().split(", ")

template = """你是一个能够生成以逗号分隔列表的助手。
用户会输入一个类别，然后你需要生成该类别中的 8 个对象，并以逗号分隔的列表形式返回。
仅返回以逗号分隔的列表，不要返回其他内容。"""
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

# 获取API密钥
minimax_api_key = os.getenv("MINIMAX_API_KEY")

# 确保API密钥存在
if not minimax_api_key:
    raise ValueError("MINIMAX_API_KEY 必须在.env文件中设置")

# 初始化LLM
llm = ChatOpenAI(
    model=os.getenv("MINIMAX_MODEL_NAME", "MiniMax-M2.5"),  # 或 "deepseek-reasoner"
    openai_api_key=minimax_api_key,
    openai_api_base="https://api.minimax.chat/v1",
    temperature=0.7,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# 创建链（使用管道方式）
chain = chat_prompt | llm | CommaSeparatedListOutputParser()

# 运行链并打印结果
result = chain.invoke({"text": "colors"})
print("生成的颜色列表:", result)
# 预期输出类似: ['red', 'blue', 'green', 'yellow', 'orange']