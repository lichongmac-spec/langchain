from typing_extensions import TypedDict, Annotated
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

class MovieDict(TypedDict):
    """电影详情字典。"""
    title: Annotated[str, ..., "电影的标题"]
    year: Annotated[int, ..., "电影上映的年份"]
    director: Annotated[str, ..., "电影的导演"]
    rating: Annotated[float, ..., "电影的评分（满分10分）"]

# 定义DeepSeek模型服务
model = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # 其他参数...
)

model_with_structure = model.with_structured_output(MovieDict)
response = model_with_structure.invoke("提供关于电影《盗梦空间》的详细信息")
print(response)  # {'title': '盗梦空间', 'year': 2010, 'director': '克里斯托弗·诺兰', 'rating': 8.8}