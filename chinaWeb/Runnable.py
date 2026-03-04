import os
import sys

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 添加上级目录到Python路径
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, parent_dir)

from langchain_core.prompts import ChatPromptTemplate
from minimax_service import get_minimax_llm

model = get_minimax_llm()
prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
chain = prompt | model

# 链的输入模式是其第一个部分（prompt）的输入模式。
result=chain.input_schema.schema()

result2=prompt.input_schema.schema()

result3=model.input_schema.schema()
# 测试模型
topic = "cats"
result = chain.invoke({"topic": topic})
print(f"关于 {topic} 的笑话: {result.content}")