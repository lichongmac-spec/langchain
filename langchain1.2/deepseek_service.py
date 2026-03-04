# deepseek_service.py
# 提供DeepSeek模型的公共服务接口，方便项目内其他文件调用

import os
import asyncio
from dotenv import load_dotenv
from langchain_core.runnables import RunnableConfig
from langchain_deepseek import ChatDeepSeek

# 加载.env文件中的环境变量
load_dotenv()

class DeepSeekService:
    """
    DeepSeek模型服务类
    提供便捷的DeepSeek模型初始化和调用接口
    """
    
    def __init__(self, model_name=None, temperature=0.7, max_retries=2):
        """
        初始化DeepSeek服务
        
        参数:
            model_name (str, optional): 要使用的模型名称，默认从环境变量获取或使用"deepseek-chat"
            temperature (float, optional): 生成文本的随机性（0.0-2.0），默认0.7
            max_retries (int, optional): 最大重试次数，默认2
        
        异常:
            ValueError: 当DEEPSEEK_API_KEY未设置时抛出
        """
        # 获取API密钥
        self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
        
        # 确保API密钥存在
        if not self.deepseek_api_key:
            raise ValueError("DEEPSEEK_API_KEY 必须在.env文件中设置")
        
        # 设置模型名称
        self.model_name = model_name or os.getenv("DEEPSEEK_MODEL_NAME", "deepseek-chat")
        
        # 初始化模型
        self.llm = ChatDeepSeek(
            model=self.model_name,
            temperature=temperature,
            max_tokens=None,
            timeout=None,
            max_retries=max_retries,
        )
    
    def get_llm(self):
        """
        获取初始化的LLM实例
        
        返回:
            ChatDeepSeek: 初始化好的DeepSeek模型实例
        """
        return self.llm
    
    def invoke(self, prompt, **kwargs):
        """
        直接调用模型生成响应
        
        参数:
            prompt (str | list): 输入提示，可以是字符串或消息列表
            **kwargs: 其他传递给模型invoke方法的参数
        
        返回:
            AIMessage: 模型生成的响应对象
        """
        response = self.llm.invoke(prompt, **kwargs)
        return response
    
    def stream(self, prompt, **kwargs):
        """
        流式调用模型生成响应
        
        参数:
            prompt (str | list): 输入提示，可以是字符串或消息列表
            **kwargs: 其他传递给模型stream方法的参数
        
        返回:
            生成器: 产生AIMessageChunk对象的生成器
        """
        return self.llm.stream(prompt, **kwargs)
    
    async def astream_events(self, prompt, config: RunnableConfig = None, **kwargs):
        """
        异步流式获取模型生成事件
        
        参数:
            prompt (str | list): 输入提示，可以是字符串或消息列表
            config (RunnableConfig, optional): 运行配置
            **kwargs: 其他传递给模型astream_events方法的参数
        
        返回:
            异步生成器: 产生事件字典的异步生成器
        """
        async for event in self.llm.astream_events(prompt, config=config, **kwargs):
            yield event

# 创建一个默认的DeepSeek服务实例
# 方便其他模块直接导入使用
default_deepseek_service = DeepSeekService()

def get_deepseek_llm():
    """
    获取默认的DeepSeek LLM实例
    
    返回:
        ChatDeepSeek: 默认的DeepSeek模型实例
    """
    return default_deepseek_service.get_llm()

def invoke_deepseek(prompt, **kwargs):
    """
    使用默认服务调用DeepSeek模型
    
    参数:
        prompt (str | list): 输入提示，可以是字符串或消息列表
        **kwargs: 其他传递给模型invoke方法的参数
    
    返回:
        AIMessage: 模型生成的响应对象
    """
    return default_deepseek_service.invoke(prompt, **kwargs)

def stream_deepseek(prompt, **kwargs):
    """
    使用默认服务流式调用DeepSeek模型
    
    参数:
        prompt (str | list): 输入提示，可以是字符串或消息列表
        **kwargs: 其他传递给模型stream方法的参数
    
    返回:
        生成器: 产生AIMessageChunk对象的生成器
    """
    return default_deepseek_service.stream(prompt, **kwargs)

async def astream_events_deepseek(prompt, config: RunnableConfig = None, **kwargs):
    """
    使用默认服务异步流式获取模型生成事件
    
    参数:
        prompt (str | list): 输入提示，可以是字符串或消息列表
        config (RunnableConfig, optional): 运行配置
        **kwargs: 其他传递给模型astream_events方法的参数
    
    返回:
        异步生成器: 产生事件字典的异步生成器
    """
    async for event in default_deepseek_service.astream_events(prompt, config=config, **kwargs):
        yield event

# 将异步事件流包装为同步迭代
def sync_astream_events(prompt: str, model=None, config: RunnableConfig = None):
    """
    将 model.astream_events 转为同步迭代器，供外部 for 循环使用。
    
    参数:
        prompt (str | list): 输入提示，可以是字符串或消息列表
        model (ChatDeepSeek, optional): 模型实例，默认使用默认服务的模型
        config (RunnableConfig, optional): 运行配置
    
    返回:
        生成器: 产生事件字典的同步生成器
    """
    if model is None:
        model = get_deepseek_llm()
    
    loop = asyncio.get_event_loop()
    aiter = model.astream_events(prompt, config=config)
    
    while True:
        try:
            yield loop.run_until_complete(aiter.__anext__())
        except StopAsyncIteration:
            break
        except Exception as e:
            raise e


# 示例用法
if __name__ == "__main__":
    """
    示例：如何使用DeepSeekService
    """
    
    print("=== 使用默认服务 ===")
    response = invoke_deepseek("你好")
    print(f"响应: {response.content}")
    
    print("\n=== 使用默认服务进行流式调用 ===")
    full = None
    for chunk in stream_deepseek("What color is the sky?"):
        full = chunk if full is None else full + chunk
        print(full.content, end="\r")
    print()
    
    print("\n=== 使用同步包装的事件流 ===")
    for event in sync_astream_events("Hello"):
        if event["event"] == "on_chat_model_start":
            print(f"输入: {event['data']['input']}")
        elif event["event"] == "on_chat_model_stream":
            print(f"Token: {event['data']['chunk'].content}")
        elif event["event"] == "on_chat_model_end":
            print(f"完整消息: {event['data']['output'].content}")
    
    print("\n=== 使用自定义服务实例 ===")
    custom_service = DeepSeekService(temperature=0.9, model_name="deepseek-chat")
    llm = custom_service.get_llm()
    response = llm.invoke("请列出5种常见的水果")
    print(f"响应: {response.content}")
    
    print("\n=== 使用消息列表 ===")
    messages = [
        ("system", "You are a helpful assistant that translates English to French. Translate the user sentence."),
        ("human", "I love programming."),
    ]
    response = invoke_deepseek(messages)
    print(f"翻译结果: {response.content}")
