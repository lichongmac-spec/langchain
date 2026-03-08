from langchain.agents import create_agent
from langchain.tools import tool
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import MemorySaver
import os
from langchain_deepseek import ChatDeepSeek
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
# 加载.env文件中的环境变量
load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add_messages]

model = ChatDeepSeek(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    timeout=None,
    stop=None,
    # thinking={"type": "enabled", "budget_tokens": 5000},  # ChatDeepSeek 不支持此参数
)


@tool
def send_email(to: str, subject: str, body: str) -> dict:
    """
    Send an email. Requires human approval.
    发送邮件。需要人工审批。
    """
    return {
        "status": "success",
        "content": f'Email sent to {to} with subject "{subject}"',
    }

@tool
def delete_file(path: str) -> dict:
    """
    Delete a file. Requires human approval.
    删除文件。需要人工审批。
    """
    return {"status": "success", "content": f'File "{path}" deleted'}

@tool
def read_file(path: str) -> dict:
    """
    Read file contents. No approval needed.
    读取文件内容。无需审批。
    """
    return {"status": "success", "content": f"Contents of {path}..."}

agent = create_agent(
    model=model,
    tools=[send_email, delete_file, read_file],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "send_email": {
                    "allowed_decisions": ["approve", "edit", "reject"],
                    # Review email before sending
                    # 发送前审核邮件
                    "description": "📧 Review email before sending\n发送前审核邮件",
                },
                "delete_file": {
                    "allowed_decisions": ["approve", "reject"],
                    # Confirm file deletion
                    # 确认文件删除
                    "description": "🗑️ Confirm file deletion\n确认文件删除",
                },
                # Safe - auto-approved
                # 安全 - 自动批准
                "read_file": False,
            }
        ),
    ],
    checkpointer=MemorySaver(),
)