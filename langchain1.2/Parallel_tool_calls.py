from langchain.tools import tool

# 导入DeepSeek服务
from deepseek_service import get_deepseek_llm

@tool
def get_weather(location: str) -> str:
    """获取指定位置的天气信息。"""
    return f"{location}的天气晴朗！"

# 并行工具调用

# 获取DeepSeek模型实例
model = get_deepseek_llm()

model_with_tools = model.bind_tools([get_weather])

# 增加system prompt，明确告诉模型在需要时应该生成多个工具调用
messages = [
    {
        "role": "system",
        "content": "你是一个能够调用工具的助手。当用户询问多个地点的天气时，你应该为每个地点生成一个单独的工具调用。"
    },
    {
        "role": "user",
        "content": "波士顿和东京的天气怎么样？"
    }
]

response = model_with_tools.invoke(messages)


# 模型可能会生成多个工具调用
print(response.tool_calls)
# [
#   {'name': 'get_weather', 'args': {'location': 'Boston'}, 'id': 'call_1'},
#   {'name': 'get_weather', 'args': {'location': 'Tokyo'}, 'id': 'call_2'},
# ]


# 执行所有工具（可以使用async进行并行处理）
results = []
for tool_call in response.tool_calls:
    if tool_call['name'] == 'get_weather':
        result = get_weather.invoke(tool_call)
    results.append(result)

# 打印结果
print("\n工具调用结果：")
for i, result in enumerate(results):
    print(f"结果 {i+1}: {result}")