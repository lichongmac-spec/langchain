import sys
import os

# 设置Python路径
sys.path.insert(0, '/Users/lichong/Documents/AI/langchain')
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool, ToolRuntime
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.structured_output import ToolStrategy

from minimax_service import get_minimax_llm
# Define system prompt
SYSTEM_PROMPT = """Y你是个天气预报专家，说话还总爱打趣。
您有以下两种工具可用：
- 获取特定地点的天气：使用此功能获取特定地点的天气
- get_user_location：使用此功能获取用户的位置
如果用户向您询问天气，请务必了解其所在位置。如果从问题中能判断出用户指的是其所在之处，请使用 get_user_location 工具来获取其位置。"""

# Define context schema
@dataclass
class Context:
    """自定义运行时上下文模式."""
    user_id: str

# Define tools
@tool
def get_weather_for_location(city: str) -> str:
    """获取指定城市的天气信息."""
    return f"在{city}总是阳光明媚！"

@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """根据用户ID获取用户位置."""
    user_id = runtime.context.user_id
    return "Florida" if user_id == "1" else "SF"

# Configure model
# model = init_chat_model(
#     "claude-sonnet-4-5-20250929",
#     temperature=0
# )

model=get_minimax_llm()

# Define response format
@dataclass
class ResponseFormat:
    """代理响应模式."""
    # 一个幽默的回复（总是必填）
    punny_response: str
    # 如果有关于天气的有趣信息，可提供
    weather_conditions: str | None = None

# Set up memory
checkpointer = InMemorySaver()

# Create agent
agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[get_user_location, get_weather_for_location],
    context_schema=Context,
    # response_format=ToolStrategy[ResponseFormat](ResponseFormat),
    response_format=ResponseFormat,
    checkpointer=checkpointer
)

# Run agent
# `thread_id` is a unique identifier for a given conversation.
config = {"configurable": {"thread_id": "1"}}

response = agent.invoke(
    {"messages": [{"role": "user", "content": "外面的天气怎么样?"}]},
    config=config,
    context=Context(user_id="1")
)

print(response['structured_response'])
# ResponseFormat(
#     punny_response="Florida is still having a 'sun-derful' day! The sunshine is playing 'ray-dio' hits all day long! I'd say it's the perfect weather for some 'solar-bration'! If you were hoping for rain, I'm afraid that idea is all 'washed up' - the forecast remains 'clear-ly' brilliant!",
#     weather_conditions="It's always sunny in Florida!"
# )


# Note that we can continue the conversation using the same `thread_id`.
response = agent.invoke(
    {"messages": [{"role": "user", "content": "非常感谢！"}]},
    config=config,
    context=Context(user_id="1")
)

print(response['structured_response'])
# ResponseFormat(
#     punny_response="You're 'thund-erfully' welcome! It's always a 'breeze' to help you stay 'current' with the weather. I'm just 'cloud'-ing around waiting to 'shower' you with more forecasts whenever you need them. Have a 'sun-sational' day in the Florida sunshine!",
#     weather_conditions=None
# )