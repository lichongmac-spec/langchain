from pydantic import BaseModel, Field
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

class Movie(BaseModel):
    """电影详情模型。"""
    title: str = Field(..., description="电影的标题")
    year: int = Field(..., description="电影上映的年份")
    director: str = Field(..., description="电影的导演")
    rating: float = Field(..., description="电影的评分（满分10分）")

# 定义DeepSeek模型服务
model = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # 其他参数...
)

model_with_structure = model.with_structured_output(Movie)
response = model_with_structure.invoke("提供关于电影《盗梦空间》的详细信息")
print(response)  # Movie(title="盗梦空间", year=2010, director="克里斯托弗·诺兰", rating=8.8)