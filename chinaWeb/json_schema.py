import json
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

json_schema = {
    "title": "Movie",
    "description": "电影详情",
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "description": "电影的标题"
        },
        "year": {
            "type": "integer",
            "description": "电影上映的年份"
        },
        "director": {
            "type": "string",
            "description": "电影的导演"
        },
        "rating": {
            "type": "number",
            "description": "电影的评分（满分10分）"
        }
    },
    "required": ["title", "year", "director", "rating"]
}

# 定义DeepSeek模型服务
model = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # 其他参数...
)

model_with_structure = model.with_structured_output(
    json_schema,
    method="json_schema",
)
response = model_with_structure.invoke("提供关于电影《盗梦空间》的详细信息")
print(response)  # {'title': '盗梦空间', 'year': 2010, ...}