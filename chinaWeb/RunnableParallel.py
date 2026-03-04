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
from langchain_core.runnables import RunnableParallel
from minimax_service import get_minimax_llm

# 获取MiniMax模型
model = get_minimax_llm()

# LangChain 并行处理 + 事件流监控演示
print("=" * 70)
print("🎯 RunnableParallel 与 astream_events 结合演示")
print("=" * 70)
print("这个演示将同时生成笑话和诗歌，并使用astream_events实时监控处理过程\n")

# 创建笑话生成链
joke_prompt = ChatPromptTemplate.from_template("告诉我一个关于{topic}的笑话")
joke_chain = joke_prompt | model.with_config(run_name="Joke_Model") | StrOutputParser()

# 创建诗歌生成链
poem_prompt = ChatPromptTemplate.from_template("写一首关于{topic}的短诗（2行）")
poem_chain = poem_prompt | model.with_config(run_name="Poem_Model") | StrOutputParser()

# 创建并行处理链
combined = RunnableParallel(
    joke=joke_chain,
    poem=poem_chain
)

# 事件流处理函数
async def monitor_events():
    topic = "猫咪"
    print(f"📌 主题: {topic}")
    print("🔄 开始并行生成...\n")
    
    async for event in combined.astream_events(
        {"topic": topic}, 
        version="v1", 
        include_names=["Joke_Model", "Poem_Model"]
    ):
        kind = event["event"]
        event_name = event.get("name", "unknown")
        data = event.get("data", {})
        
        # 任务开始事件
        if kind == "on_chat_model_start":
            task_type = "笑话" if "Joke" in event_name else "诗歌"
            print(f"🚀 {task_type}生成任务开始...")
        
        # 模型流式输出事件
        elif kind == "on_chat_model_stream":
            if "chunk" in data:
                content = data["chunk"].content
                # 过滤掉模型的思考过程
                if not content.strip().startswith("<think>") and not content.strip().startswith("</think>"):
                    task_type = "笑话" if "Joke" in event_name else "诗歌"
                    print(f"📝 {task_type}: {content}", end="", flush=True)
        
        # 模型完成事件
        elif kind == "on_chat_model_end":
            task_type = "笑话" if "Joke" in event_name else "诗歌"
            print(f"\n✅ {task_type}生成完成！")

# 运行演示
if __name__ == "__main__":
    asyncio.run(monitor_events())