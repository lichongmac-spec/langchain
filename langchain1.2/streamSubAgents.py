from typing import Any

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.messages import AIMessage, AnyMessage,AIMessageChunk, ToolMessage
import os
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv
# 加载.env文件中的环境变量
load_dotenv()



def get_weather(city: str) -> str:
    """Get weather for a given city."""

    return f"It's always sunny in {city}!"


# weather_model = init_chat_model("openai:gpt-5.2")
weather_model = ChatDeepSeek(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    timeout=None,
    stop=None,
    # thinking={"type": "enabled", "budget_tokens": 5000},  # ChatDeepSeek 不支持此参数
)
weather_agent = create_agent(
    model=weather_model,
    tools=[get_weather],
    name="weather_agent",
)


def call_weather_agent(query: str) -> str:
    """Query the weather agent."""
    result = weather_agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    return result["messages"][-1].text


# supervisor_model = init_chat_model("openai:gpt-5.2")
supervisor_model = ChatDeepSeek(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    timeout=None,
    stop=None,
    # thinking={"type": "enabled", "budget_tokens": 5000},  # ChatDeepSeek 不支持此参数
)
agent = create_agent(
    model=supervisor_model,
    tools=[call_weather_agent],
    name="supervisor",
)

def _render_message_chunk(token: AIMessageChunk) -> None:
    if token.text:
        print(token.text, end="|")
    if token.tool_call_chunks:
        print(token.tool_call_chunks)


def _render_completed_message(message: AnyMessage) -> None:
    if isinstance(message, AIMessage) and message.tool_calls:
        print(f"Tool calls: {message.tool_calls}")
    if isinstance(message, ToolMessage):
        print(f"Tool response: {message.content_blocks}")


input_message = {"role": "user", "content": "What is the weather in Boston?"}
current_agent = None
for _, stream_mode, data in agent.stream(
    {"messages": [input_message]},
    stream_mode=["messages", "updates"],
    subgraphs=True,
):
    if stream_mode == "messages":
        token, metadata = data
        if agent_name := metadata.get("lc_agent_name"):
            if agent_name != current_agent:
                print(f"🤖 {agent_name}: ")
                current_agent = agent_name  
        if isinstance(token, AIMessage):
            _render_message_chunk(token)
    if stream_mode == "updates":
        for source, update in data.items():
            if source in ("model", "tools"):
                _render_completed_message(update["messages"][-1])