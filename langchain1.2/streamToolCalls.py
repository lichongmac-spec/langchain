from typing import Any

from langchain.agents import create_agent
from langchain.messages import AIMessage, AIMessageChunk, AnyMessage, ToolMessage
import os
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv
# 加载.env文件中的环境变量
load_dotenv()


def get_weather(city: str) -> str:
    """获取指定城市的天气。"""

    return f"{city}总是阳光明媚！"

model = ChatDeepSeek(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    timeout=None,
    stop=None,
    # thinking={"type": "enabled", "budget_tokens": 5000},  # ChatDeepSeek 不支持此参数
)
agent = create_agent(model, tools=[get_weather])


def _render_message_chunk(token: AIMessageChunk) -> None:
    if token.text:
        print(token.text, end="|")
    if token.tool_call_chunks:
        print(token.tool_call_chunks)
    # 注意：所有内容都可以通过 token.content_blocks 获取


def _render_completed_message(message: AnyMessage) -> None:
    if isinstance(message, AIMessage) and message.tool_calls:
        print(f"工具调用: {message.tool_calls}")
    if isinstance(message, ToolMessage):
        print(f"工具响应: {message.content_blocks}")


input_message = {"role": "user", "content": "波士顿的天气怎么样？"}
for stream_mode, data in agent.stream(
    {"messages": [input_message]},
    stream_mode=["messages", "updates"],
):
    if stream_mode == "messages":
        token, metadata = data
        if isinstance(token, AIMessageChunk):
            _render_message_chunk(token)
    if stream_mode == "updates":
        for source, update in data.items():
            if source in ("model", "tools"):  # `source` 捕获节点名称
                _render_completed_message(update["messages"][-1])
