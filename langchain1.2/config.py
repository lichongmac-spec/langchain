from typing_extensions import Annotated, TypedDict
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv
from langchain_core.callbacks.base import BaseCallbackHandler

# 加载.env文件中的环境变量
load_dotenv()

# 定义一个简单的回调处理器
class MyCallbackHandler(BaseCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kwargs):
        print("模型开始调用...")
    
    def on_llm_end(self, response, **kwargs):
        print("模型调用结束.")

# 实例化回调处理器
my_callback_handler = MyCallbackHandler()

# 定义DeepSeek模型服务
model = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # 其他参数...
)

response = model.invoke(
    "讲一个笑话",
    config={
        "run_name": "joke_generation",      # 此运行的自定义名称
        "tags": ["humor", "demo"],          # 用于分类的标签
        "metadata": {"user_id": "123"},     # 自定义元数据
        "callbacks": [my_callback_handler], # 回调处理器
    }
)

print(response.content)

# [{'type': 'text', 'text': '有一天，一只刺猬走进一家便利店，它转了一圈，然后走到收银台前，对店员说：“你好，请问……你们卖牙刷吗？”\n\n店员愣了一下，说：“卖是卖，但你的刺……可能需要特制的吧？”\n\n刺猬叹了口气：“唉，其实我是帮我室友买的——它是一只豪猪，昨晚吃火龙果忘刷牙了，现在满嘴红刺像荧光棒，非说自己是摇滚明星，不肯出门了。”  \n\n店员：“……”'}]
































