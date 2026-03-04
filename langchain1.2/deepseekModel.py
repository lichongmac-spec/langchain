import sys
import os

# 设置Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入DeepSeek服务
from deepseek_service import (
    DeepSeekService,
    get_deepseek_llm,
    invoke_deepseek,
    stream_deepseek,
    sync_astream_events
)

# 示例1: 使用默认服务进行基本调用
print("=== 示例1: 使用默认服务进行基本调用 ===")
response = invoke_deepseek("你好")
print(f"响应: {response.content}")

# 示例2: 使用自定义服务实例
print("\n=== 示例2: 使用自定义服务实例 ===")
custom_service = DeepSeekService(temperature=0.9, model_name="deepseek-chat")
llm = custom_service.get_llm()
response = llm.invoke("请列出5种常见的水果")
print(f"响应: {response.content}")

# 示例3: 消息列表调用
print("\n=== 示例3: 消息列表调用 ===")
messages = [
    (
        "system",
        "You are a helpful assistant that translates English to French. Translate the user sentence.",
    ),
    ("human", "I love programming."),
]
response = invoke_deepseek(messages)
print(f"翻译结果: {response.content}")

# 示例4: 流式调用
print("\n=== 示例4: 流式调用 ===")
full = None
for chunk in stream_deepseek("What color is the sky?"):
    full = chunk if full is None else full + chunk
    print(full.content, end="\r")
print()

# 示例5: 使用同步事件流
print("\n=== 示例5: 使用同步事件流 ===")
for event in sync_astream_events("Hello"):
    if event["event"] == "on_chat_model_start":
        print(f"输入: {event['data']['input']}")
    elif event["event"] == "on_chat_model_stream":
        print(f"Token: {event['data']['chunk'].content}")
    elif event["event"] == "on_chat_model_end":
        print(f"完整消息: {event['data']['output'].content}")
    else:
        pass

# 示例6: 获取LLM实例后进行调用
print("\n=== 示例6: 获取LLM实例后进行调用 ===")
llm = get_deepseek_llm()
response = llm.invoke("2+2等于多少？")
print(f"响应: {response.content}")

# 注意：要运行此示例，需要确保:
# 1. .env文件中设置了DEEPSEEK_API_KEY
# 2. 已安装langchain_deepseek模块: python3.13 -m pip install langchain_deepseek --break-system-packages
