from langchain_deepseek import ChatDeepSeek
import os
from deepagents import create_deep_agent
from dotenv import load_dotenv
load_dotenv(".env")



llm = ChatDeepSeek(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    timeout=None,
    stop=None,
    # thinking={"type": "enabled", "budget_tokens": 5000},  # ChatDeepSeek 不支持此参数
)

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_deep_agent(
    model=llm,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# Run the agent
result=agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)
print(result)



