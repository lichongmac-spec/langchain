from dataclasses import dataclass
from langchain.agents import create_agent

from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

# 数据类：带有类型注解的Python数据类。返回dict类型。
@dataclass
class ContactInfo:
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
    # tools=tools,
    response_format=ContactInfo  # Auto-selects ProviderStrategy
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Extract contact info from: John Doe, john@example.com, (555) 123-4567"}]
})

print(result["structured_response"])
# {'name': 'John Doe', 'email': 'john@example.com', 'phone': '(555) 123-4567'}
# ContactInfo(name='John Doe', email='john@example.com', phone='(555) 123-4567')