# minimax_service_example.py
# 展示如何在项目内其他文件中使用MiniMax公共服务

# 方法1：导入默认的LLM实例
from minimax_service import get_minimax_llm

# 方法2：导入直接调用函数
from minimax_service import invoke_minimax

# 方法3：导入完整的服务类
from minimax_service import MiniMaxService

# 方法1示例：获取默认LLM实例并使用
print("=== 方法1：使用默认LLM实例 ===")
try:
    llm = get_minimax_llm()
    response = llm.invoke("什么是人工智能？")
    print(f"AI的定义: {response.content}")
except Exception as e:
    print(f"方法1执行出错: {e}")

# 方法2示例：直接调用函数
print("\n=== 方法2：直接调用invoke_minimax函数 ===")
try:
    response = invoke_minimax("请解释机器学习的基本概念")
    print(f"机器学习概念: {response.content}")
except Exception as e:
    print(f"方法2执行出错: {e}")

# 方法3示例：创建自定义服务实例
print("\n=== 方法3：使用自定义服务实例 ===")
try:
    # 创建一个温度更低的服务实例（生成内容更确定）
    custom_service = MiniMaxService(temperature=0.1)
    
    # 获取LLM实例
    custom_llm = custom_service.get_llm()
    
    # 使用自定义LLM
    response = custom_llm.invoke("10的平方是多少？")
    print(f"10的平方: {response.content}")
    
    # 直接使用服务的invoke方法
    response = custom_service.invoke("请列出3种编程语言")
    print(f"编程语言: {response.content}")
    
except Exception as e:
    print(f"方法3执行出错: {e}")

# 在LangChain链中使用示例
print("\n=== 在LangChain链中使用 ===")
try:
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    
    # 创建提示模板
    prompt = ChatPromptTemplate.from_template("请用{language}说'你好，世界'")
    
    # 获取默认LLM
    llm = get_minimax_llm()
    
    # 创建输出解析器
    output_parser = StrOutputParser()
    
    # 创建链
    chain = prompt | llm | output_parser
    
    # 调用链
    result = chain.invoke({"language": "西班牙语"})
    print(f"西班牙语'你好，世界': {result}")
    
except ImportError as e:
    print(f"缺少依赖: {e}")
except Exception as e:
    print(f"链执行出错: {e}")
