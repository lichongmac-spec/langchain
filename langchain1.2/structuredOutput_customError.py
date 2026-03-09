from langchain.agents.structured_output import StructuredOutputValidationError
from langchain.agents.structured_output import MultipleStructuredOutputsError
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from typing import Union
from pydantic import BaseModel, Field

from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv


# 加载.env文件中的环境变量
load_dotenv()


class ContactInfo(BaseModel):
    name: str = Field(description="Contact name")
    email: str = Field(description="Contact email")
    phone: str = Field(description="Contact phone number")

class EventDetails(BaseModel):
    name: str = Field(description="Event name")
    location: str = Field(description="Event location")
    time: str = Field(description="Event time")





def custom_error_handler(error: Exception) -> str:
    if isinstance(error, StructuredOutputValidationError):
        return "There was an issue with the format. Try again."
    elif isinstance(error, MultipleStructuredOutputsError):
        return "Multiple structured outputs were returned. Pick the most relevant one."
    else:
        return f"Error: {str(error)}"
model = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # 其他参数...
)



agent = create_agent(
    model=model,
    tools=[],
    response_format=ToolStrategy(
                        schema=Union[ContactInfo, EventDetails],
                        handle_errors=custom_error_handler
                    )  # Default: handle_errors=True
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Extract info: John Doe (john@email.com) is organizing Tech Conference on March 15th"}]
})

for msg in result['messages']:
    # If message is actually a ToolMessage object (not a dict), check its class name
    if type(msg).__name__ == "ToolMessage":
        print(msg)
    # If message is a dictionary or you want a fallback
    elif isinstance(msg, dict) and msg.get('tool_call_id'):
        print(msg)

# content="Returning structured response: name='John Doe' email='john@email.com' phone=''" name='ContactInfo' id='c12696f7-1b8e-43cf-996b-1277fece604d' tool_call_id='call_00_WydWUfQm0VzmkHQM1d3Qf0Rc'