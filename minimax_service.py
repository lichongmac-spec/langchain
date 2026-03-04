# minimax_service.py
# 提供MiniMax模型的公共服务接口，方便项目内其他文件调用

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model
# 加载.env文件中的环境变量
load_dotenv()

class MiniMaxService:
    """
    MiniMax模型服务类
    提供便捷的MiniMax模型初始化和调用接口
    """
    
    def __init__(self, model_name=None, temperature=0.7, max_retries=2):
        """
        初始化MiniMax服务
        
        参数:
            model_name (str, optional): 要使用的模型名称，默认从环境变量获取或使用"MiniMax-M2.5"
            temperature (float, optional): 生成文本的随机性（0.0-2.0），默认0.7
            max_retries (int, optional): 最大重试次数，默认2
        
        异常:
            ValueError: 当MINIMAX_API_KEY未设置时抛出
        """
        # 获取API密钥
        self.minimax_api_key = os.getenv("MINIMAX_API_KEY")
        
        # 确保API密钥存在
        if not self.minimax_api_key:
            raise ValueError("MINIMAX_API_KEY 必须在.env文件中设置")
        
        # 设置模型名称
        self.model_name = model_name or os.getenv("MINIMAX_MODEL_NAME", "MiniMax-M2.5")
        
        # 初始化模型
        self.llm = ChatOpenAI(
            model=self.model_name,
            openai_api_key=self.minimax_api_key,
            openai_api_base="https://api.minimax.chat/v1",
            temperature=temperature,
            max_tokens=None,
            timeout=None,
            max_retries=max_retries,
        )
    
    def get_llm(self):
        """
        获取初始化的LLM实例
        
        返回:
            ChatOpenAI: 初始化好的MiniMax模型实例
        """
        return self.llm
    
    def invoke(self, prompt, **kwargs):
        """
        直接调用模型生成响应
        
        参数:
            prompt (str): 输入提示
            **kwargs: 其他传递给模型invoke方法的参数
        
        返回:
            str: 模型生成的响应内容
        """
        response = self.llm.invoke(prompt, **kwargs)
        return response

# 创建一个默认的MiniMax服务实例
# 方便其他模块直接导入使用
default_minimax_service = MiniMaxService()

def get_minimax_llm():
    """
    获取默认的MiniMax LLM实例
    
    返回:
        ChatOpenAI: 默认的MiniMax模型实例
    """
    return default_minimax_service.get_llm()

def invoke_minimax(prompt, **kwargs):
    """
    使用默认服务调用MiniMax模型
    
    参数:
        prompt (str): 输入提示
        **kwargs: 其他传递给模型invoke方法的参数
    
    返回:
        str: 模型生成的响应内容
    """
    return default_minimax_service.invoke(prompt, **kwargs)


# 示例用法
if __name__ == "__main__":
    """
    示例：如何使用MiniMaxService
    """
    
    # 方法1：使用默认服务
    print("=== 使用默认服务 ===")
    response = invoke_minimax("你好，能给我讲个笑话吗？")
    print(f"响应: {response.content}")
    
    # 方法2：创建自定义服务实例
    print("\n=== 使用自定义服务实例 ===")
    custom_service = MiniMaxService(temperature=0.9)
    llm = custom_service.get_llm()
    response = llm.invoke("请列出5种常见的水果")
    print(f"响应: {response.content}")
    
    # 方法3：直接调用服务的invoke方法
    print("\n=== 直接调用服务的invoke方法 ===")
    response = custom_service.invoke("2+2等于多少？")
    print(f"响应: {response.content}")
