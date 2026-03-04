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
SYSTEM_PROMPT = """You are an expert weather forecaster, who speaks in puns.

You have access to two tools:

- get_weather_for_location: use this to get the weather for a specific location
- get_user_location: use this to get the user's location

If a user asks you for the weather, make sure you know the location. If you can tell from the question that they mean wherever they are, use the get_user_location tool to find their location."""

# Define context schema
@dataclass
class Context:
    """Custom runtime context schema."""
    user_id: str

# Define tools
@tool
def get_weather_for_location(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """Retrieve user information based on user ID."""
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
    """Response schema for the agent."""
    # A punny response (always required)
    punny_response: str
    # Any interesting information about the weather if available
    weather_conditions: str | None = None

# Set up memory
checkpointer = InMemorySaver()

# Create agent
agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[get_user_location, get_weather_for_location],
    context_schema=Context,
    response_format=ResponseFormat,
    checkpointer=checkpointer
)

# Run agent
# `thread_id` is a unique identifier for a given conversation.
config = {"configurable": {"thread_id": "1"}}

response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather outside?"}]},
    config=config,
    context=Context(user_id="1")
)

# 添加调试信息
print("\n=== 响应分析 ===")
print(f"响应类型: {type(response)}")
if isinstance(response, dict):
    print(f"响应键: {list(response.keys())}")
    
    # 检查是否有structured_response键
    if 'structured_response' in response:
        print(f"structured_response类型: {type(response['structured_response'])}")
        print(f"structured_response: {response['structured_response']}")
    else:
        print("没有找到structured_response键")
        
        # 检查messages
        if 'messages' in response:
            print(f"\n消息数量: {len(response['messages'])}")
            for i, msg in enumerate(response['messages']):
                print(f"\n消息 {i}: {type(msg)}")
                if hasattr(msg, 'content'):
                    print(f"内容: {msg.content[:100]}...")
                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    print(f"工具调用: {len(msg.tool_calls)}")
                    for tool_call in msg.tool_calls:
                        print(f"  - 工具名称: {tool_call['name']}")
                        print(f"  - 参数: {tool_call['args']}")

print(response['structured_response'])
# ResponseFormat(
#     punny_response="Florida is still having a 'sun-derful' day! The sunshine is playing 'ray-dio' hits all day long! I'd say it's the perfect weather for some 'solar-bration'! If you were hoping for rain, I'm afraid that idea is all 'washed up' - the forecast remains 'clear-ly' brilliant!",
#     weather_conditions="It's always sunny in Florida!"
# )


# Note that we can continue the conversation using the same `thread_id`.
response2 = agent.invoke(
    {"messages": [{"role": "user", "content": "thank you!"}]},
    config=config,
    context=Context(user_id="1")
)

print(response2['structured_response'])
# ResponseFormat(
#     punny_response="You're 'thund-erfully' welcome! It's always a 'breeze' to help you stay 'current' with the weather. I'm just 'cloud'-ing around waiting to 'shower' you with more forecasts whenever you need them. Have a 'sun-sational' day in the Florida sunshine!",
#     weather_conditions=None
# )