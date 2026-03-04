from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

# 定义DeepSeek模型服务
model = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # 其他参数...
)

response = model.invoke("创建一张猫的图片")
print(response.content)
# 注意：DeepSeek模型不支持直接生成图片，这里仅演示文本响应
# 输出："抱歉，我目前不支持直接生成图片。不过我可以帮你描述猫的外观或提供相关信息..."