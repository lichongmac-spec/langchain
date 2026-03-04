import os
import sys
import asyncio

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 添加上级目录到Python路径
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, parent_dir)

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from minimax_service import get_minimax_llm

# 获取MiniMax模型
model = get_minimax_llm()

print("=" * 70)
print("🎯 LangChain 并行处理 + 事件流监控演示")
print("=" * 70)
print("这个演示将同时生成关于Python的笑话和诗歌，并实时显示处理过程\n")

# 创建笑话生成链
joke_prompt = ChatPromptTemplate.from_template("告诉我一个关于{topic}的有趣笑话，保持简短有趣")
joke_chain = joke_prompt | model.with_config(run_name="Joke_Generator") | StrOutputParser()

# 创建诗歌生成链
poem_prompt = ChatPromptTemplate.from_template("写一首关于{topic}的短诗，2-4行，要有意境")
poem_chain = poem_prompt | model.with_config(run_name="Poem_Generator") | StrOutputParser()

# 创建事实信息链
fact_prompt = ChatPromptTemplate.from_template("告诉我一个关于{topic}的有趣事实")
fact_chain = fact_prompt | model.with_config(run_name="Fact_Generator") | StrOutputParser()

# 创建并行处理链
parallel_chain = RunnableParallel(
    joke=joke_chain,
    poem=poem_chain,
    fact=fact_chain
)

# 处理事件流的函数
async def handle_events():
    topic = "Python编程语言"
    print(f"📌 主题: {topic}")
    print("🔄 开始并行生成...\n")
    
    # 用于跟踪各个任务的完成状态
    completed_tasks = {}
    
    async for event in parallel_chain.astream_events(
        {"topic": topic}, 
        version="v1", 
        include_names=["Joke_Generator", "Poem_Generator", "Fact_Generator"]
    ):
        kind = event["event"]
        event_name = event.get("name", "unknown")
        data = event.get("data", {})
        
        # 任务开始事件
        if kind == "on_chat_model_start":
            task_type = event_name.replace("_Generator", "")
            print(f"🚀 {task_type} 任务开始处理...")
            completed_tasks[event_name] = False
        
        # 模型流式输出事件
        elif kind == "on_chat_model_stream":
            if "chunk" in data:
                content = data["chunk"].content
                # 过滤掉模型的思考过程
                if not content.strip().startswith("<think>") and not content.strip().startswith("</think>"):
                    task_type = event_name.replace("_Generator", "")
                    print(f"📝 {task_type}: {content}", end="", flush=True)
        
        # 模型完成事件
        elif kind == "on_chat_model_end":
            task_type = event_name.replace("_Generator", "")
            print(f"\n✅ {task_type} 任务完成！")
            completed_tasks[event_name] = True
            
            # 检查是否所有任务都已完成
            if all(completed_tasks.values()):
                print("\n🎊 所有并行任务处理完成！")
                break
        
        # 解析器完成事件
        elif kind == "on_parser_end":
            task_type = event_name.replace("_Generator", "")
            print(f"📋 {task_type} 输出解析完成")

# 运行演示
if __name__ == "__main__":
    asyncio.run(handle_events())
