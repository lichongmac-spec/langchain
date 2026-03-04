import os
import sys

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 添加上级目录到Python路径
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, parent_dir)

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from minimax_service import get_minimax_llm
from deepseek_service import get_deepseek_llm

# 创建提示模板
prompt = ChatPromptTemplate.from_template("告诉我关于{topic}的有趣事实")

# 创建输出解析器
output_parser = StrOutputParser()

# 获取MiniMax和DeepSeek模型
minimax_llm = get_minimax_llm()
deepseek_llm = get_deepseek_llm()

print("=" * 70)
print("🎯 LCEL 多模型演示")
print("=" * 70)

# 创建一个简单的函数来根据选择的模型创建链
def create_chain(selected_model):
    llm = minimax_llm if selected_model == "minimax" else deepseek_llm
    return {
        "topic": RunnablePassthrough()
    } | prompt | llm | output_parser

# 使用MiniMax模型
print("\n1. 使用MiniMax模型:")
minimax_chain = create_chain("minimax")
result1 = minimax_chain.invoke("冰淇淋")
print(f"结果: {result1}")

# 使用DeepSeek模型
print("\n2. 使用DeepSeek模型:")
deepseek_chain = create_chain("deepseek")
result2 = deepseek_chain.invoke("意大利面")
print(f"结果: {result2}")

# 批量处理
print("\n3. 批量处理 (使用MiniMax模型):")
results = minimax_chain.batch(["冰淇淋", "意大利面", "饺子"])
for i, result in enumerate(results, 1):
    print(f"  {i}. {result}")

print("\n✅ 演示完成！")
