from langchain.agents import create_agent
from langchain.agents.structured_output import ProviderStrategy
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv



# 加载.env文件中的环境变量
load_dotenv()



contact_info_schema = {
    "type": "object",
    "description": "Contact information for a person.",
    "properties": {
        "name": {"type": "string", "description": "The name of the person"},
        "email": {"type": "string", "description": "The email address of the person"},
        "phone": {"type": "string", "description": "The phone number of the person"}
    },
    "required": ["name", "email", "phone"]
}
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
    response_format=contact_info_schema
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Extract contact info from: John Doe, john@example.com, (555) 123-4567"}]
})
# {'name': 'John Doe', 'email': 'john@example.com', 'phone': '(555) 123-4567'}
print(result["structured_response"])
# {'name': 'John Doe', 'email': 'john@example.com', 'phone': '(555) 123-4567'}