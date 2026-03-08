from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from typing import TypedDict, Annotated
import os
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv
# 加载.env文件中的环境变量
load_dotenv()



class State(TypedDict):
    messages: Annotated[list, add_messages]

# model = ChatOpenAI(model="gpt-4.1-mini")
model = ChatDeepSeek(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    timeout=None,
    stop=None,
    # thinking={"type": "enabled", "budget_tokens": 5000},  # ChatDeepSeek 不支持此参数
)

async def agent(state: State) -> dict:
    response = await model.ainvoke(state["messages"])
    return {"messages": [response]}

workflow = StateGraph(State)
workflow.add_node("agent", agent)
workflow.add_edge(START, "agent")
workflow.add_edge("agent", END)

graph = workflow.compile()

result = graph.ainvoke({"messages": ["你好"]})
print(result)