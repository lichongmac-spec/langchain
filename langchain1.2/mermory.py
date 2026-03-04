from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_deepseek import ChatDeepSeek
import os

# Load environment variables from .env file
if os.path.exists('.env'):
    with open('.env', 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                os.environ.setdefault(key.strip(), value.strip())
# 示例工具函数
def get_user_info():
    """获取用户信息的工具"""
    pass

model=ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

agent = create_agent(
    model=model,
    tools=[get_user_info],
    checkpointer=InMemorySaver(),
)

res=agent.invoke(
    {"messages": [{"role": "user", "content": "Hi! My name is Bob."}]},
    {"configurable": {"thread_id": "1"}},
)

print(res)