from typing_extensions import TypedDict
from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv


# 加载.env文件中的环境变量
load_dotenv()
# 类型化字典类。返回dict类型
class ContactInfo(TypedDict):
    """Contact information for a person."""
    name: str # The name of the person
    email: str # The email address of the person
    phone: str # The phone number of the person

model=ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # 其他参数...
)   



agent = create_agent(
    model=model,
    response_format=ContactInfo  # Auto-selects ProviderStrategy
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Extract contact info from: John Doe, john@example.com, (555) 123-4567"}]
})
# {'name': 'John Doe', 'email': 'john@example.com', 'phone': '(555) 123-4567'} 亲测
print(result["structured_response"])
# {'name': 'John Doe', 'email': 'john@example.com', 'phone': '(555) 123-4567'}