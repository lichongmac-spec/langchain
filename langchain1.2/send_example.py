"""
LangGraph Send 简单使用示例

Send 类用于在条件边中动态地将状态发送到多个节点，实现并行执行。
"""

from langgraph.graph import StateGraph, START, END, Send
from typing import TypedDict, Annotated
import operator


# 定义状态类型
class State(TypedDict):
    messages: Annotated[list[str], operator.add]  # 使用 operator.add 合并列表
    items: list[str]


# 节点1: 初始化，设置要处理的 items
def init_node(state: State) -> dict:
    return {
        "items": ["apple", "banana", "cherry"],
        "messages": ["初始化完成"]
    }


# 节点2: 处理单个 item（会被并行调用多次）
def process_item(state: State) -> dict:
    # 获取当前要处理的 item
    item = state.get("current_item", "unknown")
    result = f"处理了: {item}"
    return {
        "messages": [result]
    }


# 条件边函数: 使用 Send 将状态分发到多个节点
# 返回 Send 对象列表，每个 Send 对象指定目标节点和状态
def fan_out_to_process(state: State) -> list[Send]:
    items = state.get("items", [])
    
    # 为每个 item 创建一个 Send 对象
    # Send("节点名称", 传递给节点的状态)
    return [
        Send("process_item", {"current_item": item, "messages": []})
        for item in items
    ]


# 节点3: 收集结果
def collect_results(state: State) -> dict:
    messages = state.get("messages", [])
    summary = f"总共处理了 {len(messages)} 个消息"
    return {
        "messages": [summary]
    }


# 构建工作流
workflow = StateGraph(State)

# 添加节点
workflow.add_node("init", init_node)
workflow.add_node("process_item", process_item)
workflow.add_node("collect", collect_results)

# 添加边
workflow.add_edge(START, "init")

# 使用 add_conditional_edges 和 Send 实现并行处理
# fan_out_to_process 返回多个 Send 对象，每个对象触发一次 process_item 节点
workflow.add_conditional_edges("init", fan_out_to_process)

# 从 process_item 收集结果后，进入 collect 节点
workflow.add_edge("process_item", "collect")
workflow.add_edge("collect", END)

# 编译工作流
app = workflow.compile()
app

# 运行工作流
if __name__ == "__main__":
    # 初始状态
    initial_state = {
        "messages": [],
        "items": []
    }
    
    # 运行
    result = app.invoke(initial_state)
    
    print("最终结果:")
    for msg in result["messages"]:
        print(f"  - {msg}")
