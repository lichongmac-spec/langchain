from langchain.chains import LLMMathChain
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_core.tools import Tool
from langchain_experimental.plan_and_execute import (
    PlanAndExecute,
    load_agent_executor,
    load_chat_planner,
)
import os
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

# 使用DeepSeek模型服务
from deepseek_service import get_deepseek_llm

try:
    # 使用DeepSeek服务获取模型实例
    llm = get_deepseek_llm()
    
    # 创建数学计算链
    llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)

    # 设置搜索工具
    search = DuckDuckGoSearchAPIWrapper()
    search_tool = Tool(
        name="Search",
        func=search.run,
        description="此工具适用于您需要回答有关当前事件或获取网络信息的情况。"
    )
    
    # 设置工具列表
    tools = [
        Tool(
            name="Calculator",
            func=llm_math_chain.invoke,
            description="此工具适用于您需要回答有关数学问题的情况。"
        ),
        search_tool
    ]

    # 使用同一个DeepSeek模型实例
    chat_llm = llm

    planner = load_chat_planner(chat_llm)
    executor = load_agent_executor(chat_llm, tools, verbose=True)
    agent = PlanAndExecute(planner=planner, executor=executor, verbose=True)
    task_result = agent.run("2023年中国的GDP增长率是多少？然后计算这个数字的平方根。")
    print(f"任务结果: {task_result}")
    
except ValueError as ve:
    print(f"配置错误: {ve}")
    print("请确保在.env文件中正确设置了DEEPSEEK_API_KEY")
except Exception as e:
    print(f"执行过程中遇到错误: {type(e).__name__}: {e}")
    print("\n可能的解决方法:")
    print("1. 检查您的网络连接是否正常")
    print("2. 验证您的DEEPSEEK_API_KEY是否有效")
    print("3. 确保您的API密钥有足够的使用额度")
    print("4. 检查DeepSeek API服务是否正常运行")
    print("5. 您可以尝试降低请求频率或增加超时时间")