from pydantic import BaseModel, Field
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

class Actor(BaseModel):
    name: str
    role: str

class MovieDetails(BaseModel):
    title: str
    year: int
    cast: list[Actor]
    genres: list[str]
    budget: float | None = Field(None, description="Budget in millions USD")

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

# title='盗梦空间' year=2010 cast=[Actor(name='莱昂纳多·迪卡普里奥', role='多姆·柯布'), Actor(name='约瑟夫·高登-莱维特', role='亚瑟'), Actor(name='艾伦·佩吉', role='阿里阿德涅'), Actor(name='汤姆·哈迪', role='伊姆斯'), Actor(name='渡边谦', role='斋藤'), Actor(name='希里安·墨菲', role='罗伯特·费舍尔'), Actor(name='玛丽昂·歌迪亚', role='梅尔')] genres=['科幻', '动作', '惊悚'] budget=160.0