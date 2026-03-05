from langchain.tools import tool, ToolRuntime
from langgraph.store.memory import InMemoryStore
from langchain_deepseek import ChatDeepSeek
from langchain.agents import create_agent
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

@tool
def get_weather(city: str, runtime: ToolRuntime) -> str:
    """Get weather for a given city."""
    writer = runtime.stream_writer

    # Stream custom updates as the tool executes
    writer(f"Looking up data for city: {city}")
    writer(f"Acquired data for city: {city}")

    return f"It's always sunny in {city}!"

store = InMemoryStore()
model=ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # 其他参数...
)
agent = create_agent(
    model,
    tools=[get_weather],
    store=store
)

res=agent.invoke({"messages": [{"role": "user", "content": "获取北京的天气"}]})
print(res)