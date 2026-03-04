from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv
import asyncio
from langchain_core.runnables import RunnableConfig
# 加载.env文件中的环境变量
load_dotenv()


model = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)
for response in model.batch_as_completed([
    "W为什么鹦鹉会有色彩斑斓的羽毛呢？",
    "飞机是如何飞行的？",
    "量子计算是一种什么技术？"
]):
    print(response)

# responses = model.batch([
#     "Why do parrots have colorful feathers?",
#     "How do airplanes fly?",
#     "What is quantum computing?"
# ])
# for response in responses:
#     print(response)