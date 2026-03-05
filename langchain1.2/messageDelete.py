from langchain.messages import RemoveMessage
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import after_model
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.runtime import Runtime
from langchain_core.runnables import RunnableConfig
from langchain_deepseek import ChatDeepSeek

from dotenv import load_dotenv

load_dotenv()

@after_model
def delete_old_messages(state: AgentState, runtime: Runtime) -> dict | None:
    """Remove old messages to keep conversation manageable."""
    messages = state["messages"]
    if len(messages) > 2:
        # remove the earliest two messages
        return {"messages": [RemoveMessage(id=m.id) for m in messages[:2]]}
    return None

model=ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # 其他参数...
)

agent = create_agent(
    model,
    tools=[],
    system_prompt="Please be concise and to the point.",
    middleware=[delete_old_messages],
    checkpointer=InMemorySaver(),
)

config: RunnableConfig = {"configurable": {"thread_id": "1"}}

for event in agent.stream(
    {"messages": [{"role": "user", "content": "hi! I'm bob"}]},
    config,
    stream_mode="values",
):
    print([(message.type, message.content) for message in event["messages"]])

for event in agent.stream(
    {"messages": [{"role": "user", "content": "what's my name?"}]},
    config,
    stream_mode="values",
):
    print([(message.type, message.content) for message in event["messages"]])

# [('human', "hi! I'm bob")]
# [('human', "hi! I'm bob"), ('ai', 'Hi Bob! Nice to meet you. How can I help you today?')]
# [('human', "hi! I'm bob"), ('ai', 'Hi Bob! Nice to meet you. How can I help you today?'), ('human', "what's my name?")]
# [('human', "hi! I'm bob"), ('ai', 'Hi Bob! Nice to meet you. How can I help you today?'), ('human', "what's my name?"), ('ai', 'Your name is Bob! You introduced yourself at the beginning of our conversation.')]
# [('human', "what's my name?"), ('ai', 'Your name is Bob! You introduced yourself at the beginning of our conversation.')]