from typing_extensions import Annotated, TypedDict
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

class Actor(TypedDict):
    name: str
    role: str

class MovieDetails(TypedDict):
    title: str
    year: int
    cast: list[Actor]
    genres: list[str]
    budget: Annotated[float | None, ..., "Budget in millions USD"]

# 定义DeepSeek模型服务
model = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # 其他参数...
)

model_with_structure = model.with_structured_output(MovieDetails)

# 调用模型获取嵌套结构化输出
response = model_with_structure.invoke("提供关于电影《盗梦空间》的详细信息，包括演员、角色、类型和预算")
print(response)

# {'title': '盗梦空间', 'year': 2010, 'cast': [{'name': '莱昂纳多·迪卡普里奥', 'role': '多姆·柯布'}, {'name': '约瑟夫·高登-莱维特', 'role': '亚瑟'}, {'name': '艾伦·佩吉', 'role': '阿里亚德妮'}, {'name': '汤姆·哈迪', 'role': '伊姆斯'}, {'name': '渡边谦', 'role': '斋藤'}, {'name': '希里安·墨菲', 'role': '罗伯特·费舍尔'}, {'name': '玛丽昂·歌迪亚', 'role': '梅尔'}, {'name': '迈克尔·凯恩', 'role': '迈尔斯教授'}], 'genres': ['科幻', '动作', '惊悚', '悬疑'], 'budget': 160}