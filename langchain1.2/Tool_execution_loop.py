from langchain.tools import tool

# 导入DeepSeek服务
from deepseek_service import get_deepseek_llm

@tool
def get_weather(location: str) -> str:
    """获取指定位置的天气信息。"""
    return f"{location}的天气晴朗！"

# 获取DeepSeek模型实例
model = get_deepseek_llm()

# 将（可能多个）工具绑定到模型
model_with_tools = model.bind_tools([get_weather])

# 步骤1：模型生成工具调用
messages = [{"role": "user", "content": "波士顿的天气怎么样？"}]
ai_msg = model_with_tools.invoke(messages)
messages.append(ai_msg)

# 步骤2：执行工具并收集结果
for tool_call in ai_msg.tool_calls:
    # 使用生成的参数执行工具
    tool_result = get_weather.invoke(tool_call)
    messages.append(tool_result)

# 步骤3：将结果传递回模型以获取最终响应
final_response = model_with_tools.invoke(messages)
print(final_response.text)
# "波士顿当前天气为晴天！"