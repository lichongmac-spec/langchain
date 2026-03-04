from langchain.chains import LLMMathChain
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_core.tools import Tool
from langchain_experimental.plan_and_execute import (
    PlanAndExecute,
    load_agent_executor,
    load_chat_planner,
)
from langchain_openai import ChatOpenAI, OpenAI
from langchain_community.llms import Minimax
import os
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

# 配置要使用的LLM提供商："openai" 或 "minimax"
# 注意：当前MiniMax集成存在兼容性问题，建议暂时使用OpenAI


# 使用MiniMax模型
minimax_api_key = os.getenv("MINIMAX_API_KEY")
minimax_group_id = os.getenv("MINIMAX_GROUP_ID")

# 确保API密钥和群组ID存在
llm = ChatOpenAI(
    model=os.getenv("MINIMAX_MODEL_NAME", "MiniMax-M2.5"),  # 或 "deepseek-reasoner"
    openai_api_key=minimax_api_key,
    openai_api_base="https://api.minimax.chat/v1",
    temperature=0.7,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# 创建数学计算链
llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)

# 注意：运行以下示例需要有效的API密钥和支持的地区
# 请确保在.env文件中正确设置了相应的API密钥

try:
    # 示例1: 使用LLMMathChain进行数学计算
    print("=== 示例1: LLMMathChain数学计算 ===")
    # 使用invoke方法替代已弃用的run方法
    result = llm_math_chain.invoke("3.14159的平方是多少？")
    print(f"结果: {result}")
    
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
    
    # 示例2: 使用PlanAndExecute代理完成复杂任务
    print("\n=== 示例2: PlanAndExecute代理复杂任务 ===")
    
    chat_llm =ChatOpenAI(
                model=os.getenv("MINIMAX_MODEL_NAME", "MiniMax-M2.5"),  # 或 "deepseek-reasoner"
                openai_api_key=minimax_api_key,
                openai_api_base="https://api.minimax.chat/v1",
                temperature=0.7,
                max_tokens=None,
                timeout=None,
                max_retries=2,
            )
    
    # 创建plan and execute代理
    planner = load_chat_planner(chat_llm)
    executor = load_agent_executor(chat_llm, tools, verbose=True)
    agent = PlanAndExecute(planner=planner, executor=executor, verbose=True)
    
    # 运行一个需要搜索和计算的复杂任务
    task_result = agent.invoke("2023年中国的GDP增长率是多少？然后计算这个数字的平方根。")
    print(f"任务结果: {task_result}")
    
except Exception as e:
    print(f"\n运行示例时遇到错误: {type(e).__name__}: {e}")
    print("\n提示:")
    print("1. 请确保在.env文件中正确设置了有效的API密钥")
    
    print("4. 您也可以修改示例代码使用其他兼容的LLM模型")
    print("5. 要切换LLM提供商，修改脚本中的LLM_PROVIDER变量")
