import os
import sys

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 添加上级目录到Python路径
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, parent_dir)

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from minimax_service import get_minimax_llm

# 使用简单的文档列表和检索逻辑，避免依赖FAISS
texts = [
    "Python是一种流行的编程语言，由Guido van Rossum创建于1989年",
    "Python的设计哲学强调代码可读性和简洁性",
    "Python支持多种编程范式，包括面向对象、命令式、函数式和过程式编程",
    "Python有一个庞大的标准库和丰富的第三方包生态系统",
    "Python常用于Web开发、数据分析、人工智能、科学计算等领域"
]

# 简单的检索器函数
def simple_retriever(query):
    """基于关键词匹配的简单检索器"""
    query_lower = query.lower()
    relevant_docs = []
    for text in texts:
        if any(word in text.lower() for word in query_lower.split()):
            relevant_docs.append({"page_content": text})
    # 最多返回3个相关文档
    return relevant_docs[:3]

# 创建提示模板
template = """你是一个知识渊博的助手，根据提供的上下文回答问题。
上下文：
{context}

问题：{question}

请用中文回答，保持友好和专业。
"""
prompt = ChatPromptTemplate.from_template(template)

# 获取MiniMax模型
model = get_minimax_llm()

# 准备上下文的函数
def format_context(docs):
    """格式化文档列表为上下文文本"""
    return "\n".join(doc["page_content"] for doc in docs)

# 定义更有趣的链
fun_chain = (
    {
        "context": RunnablePassthrough() | simple_retriever | format_context,
        "question": RunnablePassthrough(),
    }
    | prompt
    | model.with_config(run_name="MiniMax_Language_Model")
    | StrOutputParser()
)

import asyncio

async def main():
    # 定义一个更有趣的问题
    question = "Python有哪些主要的应用领域？"
    print(f"\n正在处理问题: {question}")
    print("=" * 50)
    
    async for event in fun_chain.astream_events(
        question, version="v1", include_names=["MiniMax_Language_Model"]
    ):
        kind = event["event"]
        
        if kind == "on_retriever_start":
            print("🔍 正在检索相关文档...")
        
        elif kind == "on_retriever_end":
            print("📄 检索到的文档内容:")
            docs = event["data"]["output"]
            for i, doc in enumerate(docs, 1):
                print(f"   {i}. {doc['page_content']}")
            print()
            print("🤖 正在生成回答...")
            print()
        
        elif kind == "on_chat_model_start":
            print("💬 语言模型开始处理请求")
        
        elif kind == "on_chat_model_stream":
            # 实时显示模型生成的内容，使用颜色突出显示
            chunk = event["data"]["chunk"].content
            print(chunk, end="", flush=True)
        
        elif kind == "on_chat_model_end":
            print()
            print()
            print("✅ 回答生成完成")
        
        elif kind == "on_parser_start":
            print("📝 正在解析模型输出...")
        
        elif kind == "on_parser_end":
            print("📋 输出解析完成")

# 运行主函数
if __name__ == "__main__":
    asyncio.run(main())