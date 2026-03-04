from langchain.tools import tool

# 导入DeepSeek服务
from deepseek_service import get_deepseek_llm

@tool
def get_weather(location: str) -> str:
    """Get the weather at a location."""
    return f"It's sunny in {location}."


# 获取DeepSeek模型实例
model = get_deepseek_llm()

# 绑定工具到模型
model_with_tools = model.bind_tools([get_weather])  

# 调用模型
response = model_with_tools.invoke("What's the weather like in Boston?")

# 处理工具调用
for tool_call in response.tool_calls:
    # 查看模型做出的工具调用
    print(f"工具: {tool_call['name']}")
    print(f"参数: {tool_call['args']}")
    
    # 如果需要，可以执行工具并将结果返回给模型
    if tool_call['name'] == "get_weather":
        location = tool_call['args']['location']
        weather_result = get_weather.invoke(location)  # 使用invoke方法调用工具
        print(f"工具调用结果: {weather_result}")