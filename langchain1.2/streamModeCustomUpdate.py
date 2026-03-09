from langchain.agents import create_agent
from langgraph.config import get_stream_writer
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

model=ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # 其他参数...
)



def get_weather(city: str) -> str:
    """Get weather for a given city."""
    writer = get_stream_writer()
    writer(f"Looking up data for city: {city}")
    writer(f"Acquired data for city: {city}")
    return f"It's always sunny in {city}!"

agent = create_agent(
    model=model,
    tools=[get_weather],
)

for stream_mode, chunk in agent.stream(
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    stream_mode=["updates", "custom"]
):
    print(f"stream_mode: {stream_mode}")
    print(f"content: {chunk}")
    print("\n")