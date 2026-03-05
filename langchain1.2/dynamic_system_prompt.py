from langchain.agents import create_agent
from typing import TypedDict
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()



class CustomContext(TypedDict):
    user_name: str


def get_weather(city: str) -> str:
    """Get the weather in a city."""
    return f"The weather in {city} is always sunny!"


@dynamic_prompt
def dynamic_system_prompt(request: ModelRequest) -> str:
    user_name = request.runtime.context["user_name"]
    system_prompt = f"You are a helpful assistant. Address the user as {user_name}."
    return system_prompt

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
    middleware=[dynamic_system_prompt],
    context_schema=CustomContext,
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    context=CustomContext(user_name="John Smith"),
)
for msg in result["messages"]:
    msg.pretty_print()

# ================================ Human Message =================================

# What is the weather in SF?
# ================================== Ai Message ==================================

# I'll check the weather in San Francisco for you.
# Tool Calls:
#   get_weather (call_00_BHiBgdMmOmzRP69x53yEQgVu)
#  Call ID: call_00_BHiBgdMmOmzRP69x53yEQgVu
#   Args:
#     city: San Francisco
# ================================= Tool Message =================================
# Name: get_weather

# The weather in San Francisco is always sunny!
# ================================== Ai Message ==================================

# John Smith, the weather in San Francisco is always sunny!