from langchain_core.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv
import os

load_dotenv()

llm=ChatDeepSeek(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.7
)
prompt=ChatPromptTemplate.from_messages([
    ("system","你是一个专业的翻译"),
    ("human","{input}")
])

chain = prompt | llm

response=chain.invoke({"input":"你好"})
print(response.content)
