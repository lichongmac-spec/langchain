from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END, Send
from langgraph.graph.state import CompiledStateGraph
from langchain.messages import BaseMessage, AIMessage
from typing import TypedDict, Annotated
import operator

# Use different model instances for variety
analytical_model = ChatOpenAI(model="gpt-4.1-mini", temperature=0.3)
creative_model = ChatOpenAI(model="gpt-4.1-mini", temperature=0.9)
practical_model = ChatOpenAI(model="gpt-4.1-mini", temperature=0.5)

class State(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
    topic: str
    analytical_research: str
    creative_research: str
    practical_research: str

def fan_out_to_researchers(state: State) -> list[Send]:
    return [
        Send("researcher_analytical", state),
        Send("researcher_creative", state),
        Send("researcher_practical", state),
    ]

def dispatcher(state: State) -> dict:
    last_message = state["messages"][-1] if state["messages"] else None
    topic = last_message.content if last_message else ""
    return {"topic": topic}

async def researcher_analytical(state: State) -> dict:
    response = await analytical_model.ainvoke([
        {"role": "system", "content": "You are an analytical research expert."},
        {"role": "user", "content": f"Research: {state['topic']}"},
    ])
    return {
        "analytical_research": response.content,
        "messages": [AIMessage(content=response.content, name="researcher_analytical")],
    }

# Similar nodes for creative and practical researchers...

workflow = StateGraph(State)
workflow.add_node("dispatcher", dispatcher)
workflow.add_node("researcher_analytical", researcher_analytical)
workflow.add_node("researcher_creative", researcher_creative)
workflow.add_node("researcher_practical", researcher_practical)
workflow.add_edge(START, "dispatcher")
workflow.add_conditional_edges("dispatcher", fan_out_to_researchers)
workflow.add_edge("researcher_analytical", END)
workflow.add_edge("researcher_creative", END)
workflow.add_edge("researcher_practical", END)

agent: CompiledStateGraph = workflow.compile()