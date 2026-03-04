# 简化版RAG示例，使用minimax_service
# 需要安装：pip install langchain

import sys
import os

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 设置项目根目录（chinaWeb 目录的父目录）
project_root = os.path.abspath(os.path.join(current_dir, ".."))
# 将根目录添加到系统路径
sys.path.insert(0, project_root)

# 导入必要的库
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# 导入minimax服务
from minimax_service import get_minimax_llm

# 创建提示模板
prompt = ChatPromptTemplate.from_template("""
根据以下上下文回答问题：
{context}

问题：{question}
""")

# 获取minimax模型实例
model = get_minimax_llm()

# 创建输出解析器
output_parser = StrOutputParser()

# 定义上下文
context = "harrison worked at kensho\nbears like to eat honey"

# 创建链
chain = (
    {"context": lambda _: context, "question": RunnablePassthrough()}
    | prompt
    | model
    | output_parser
)

# 运行链
result = chain.invoke("where did harrison work?")
print("问题: where did harrison work?")
print("答案:", result)
