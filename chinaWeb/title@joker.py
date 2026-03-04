# 它接受一个主题并生成一个笑话

import sys
import os

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 设置项目根目录（title@joker.py 所在目录的父目录）
project_root = os.path.abspath(os.path.join(current_dir, ".."))
# 将根目录添加到系统路径
sys.path.insert(0, project_root)

# 导入必要的库和服务
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from minimax_service import get_minimax_llm

# 创建提示模板
prompt = ChatPromptTemplate.from_template("给我讲一个关于{topic}的简短笑话。")

# 使用minimax_service获取模型实例
model = get_minimax_llm()

# 创建输出解析器
output_parser = StrOutputParser()

# 创建链
chain = prompt | model | output_parser

# 运行并打印结果
# result = chain.invoke({"topic": "冰淇淋"})
# print("生成的笑话:", result)

input = {"topic": "ice cream"}

output = prompt.invoke(input)
# > ChatPromptValue(messages=[HumanMessage(content='tell me a short joke about ice cream')])

output2 = (prompt | model).invoke(input)
# > AIMessage(content="为什么冰淇淋去看心理医生？\n因为它有太多的配料，找不到自己的冰淇淋锥自信！")
print(output2.content)