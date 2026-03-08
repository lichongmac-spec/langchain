from langchain.agents import create_agent
from langchain.messages import AIMessageChunk
from langchain_core.runnables import Runnable
from langchain_deepseek import ChatDeepSeek
# from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import os
# 加载.env文件中的环境变量
load_dotenv()


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


"""
ChatDeepSeek 启用思考模式的方法：

1. 注意：ChatDeepSeek 不支持直接在构造函数中设置 thinking 字段
2. 正确的方法是在调用模型时通过 extra_body 参数传递 thinking 配置

thinking 参数的结构：
{
    "type": "enabled",  # 启用思考模式
    "budget_tokens": 5000  # 思考过程的最大 token 数
}

通过 extra_body 参数传递后，模型的响应中会包含 reasoning_content 字段
"""

# 初始化模型
model = ChatDeepSeek(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    timeout=None,
    stop=None,
    # thinking={"type": "enabled", "budget_tokens": 5000},  # ChatDeepSeek 不支持此参数
)

"""
示例1：直接调用模型时启用思考模式

在 model.invoke() 方法中通过 extra_body 参数传递 thinking 配置
"""
# print("示例1：直接调用模型时启用思考模式")
# response = model.invoke(
#     "What is the weather in San Francisco?",
#     extra_body={"thinking": {"type": "enabled", "budget_tokens": 5000}}
# )
# print(f"响应内容: {response.content}")
# 
# # 检查是否有推理内容
# if "reasoning_content" in response.additional_kwargs:
#     print(f"推理内容: {response.additional_kwargs['reasoning_content']}")

"""
示例2：流式调用模型时启用思考模式

在 model.stream() 方法中通过 extra_body 参数传递 thinking 配置
"""
# print("\n示例2：流式调用模型时启用思考模式")
# for chunk in model.stream(
#     "What is the weather in New York?",
#     extra_body={"thinking": {"type": "enabled", "budget_tokens": 5000}}
# ):
#     if isinstance(chunk, AIMessageChunk):
#         if chunk.content:
#             print(chunk.content, end="")
#         
#         # 检查是否有推理内容
#         if "reasoning_content" in chunk.additional_kwargs:
#             print(f"\n[思考] {chunk.additional_kwargs['reasoning_content']}", end="")

"""
示例3：使用 agent 时启用思考模式

注意：agent.stream() 不直接支持 extra_body 参数
若需要在 agent 中启用思考模式，需要通过其他方式，如自定义 agent 配置
"""
# agent: Runnable = create_agent(
#     model=model,
#     tools=[get_weather],
# )
# 
# for token, metadata in agent.stream(
#     {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
#     stream_mode="messages",
# ):
#     if not isinstance(token, AIMessageChunk):
#         continue
#     
#     # 检查 content_blocks
#     if hasattr(token, 'content_blocks'):
#         reasoning = [b for b in token.content_blocks if b.get("type") == "reasoning"]
#         text = [b for b in token.content_blocks if b.get("type") == "text"]
#         if reasoning:
#             print(f"[thinking] {reasoning[0].get('reasoning', '')}", end="")
#         if text:
#             print(text[0].get("text", ""), end="")
#     else:
#         # 检查 additional_kwargs 中的推理内容
#         if "reasoning_content" in token.additional_kwargs:
#             print(f"[思考] {token.additional_kwargs['reasoning_content']}", end="")
#         if token.content:
#             print(token.content, end="")

print("ChatDeepSeek 启用思考模式的方法已添加到代码注释中")
print("请参考代码中的注释和示例代码")

agent: Runnable = create_agent(
    model=model,
    tools=[get_weather],
)

for token, metadata in agent.stream(
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    stream_mode="messages",
):
    if not isinstance(token, AIMessageChunk):
        continue
    reasoning = [b for b in token.content_blocks if b["type"] == "reasoning"]
    text = [b for b in token.content_blocks if b["type"] == "text"]
    if reasoning:
        print(f"[thinking] {reasoning[0]['reasoning']}", end="")
    if text:
        print(text[0]["text"], end="")