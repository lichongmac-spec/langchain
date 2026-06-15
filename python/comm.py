# 1. datetime - 处理时间
from datetime import datetime, timedelta
now = datetime.now()
yesterday = now - timedelta(days=1)
print(yesterday.strftime("%Y-%m-%d"))

# 2. random - 随机操作
import random
items = [1,2,3,4,5]
random.shuffle(items)  # 随机打乱
sample = random.sample(items, 3)  # 随机取3个

# 3. json - 读写JSON
import json
data = {"name": "Android", "version": 14}
json_str = json.dumps(data, indent=2)  # 格式化输出
parsed = json.loads(json_str)

# 4. pathlib - 现代化路径操作（推荐替代os.path）
from pathlib import Path
p = Path("/my/project")
p / "data" / "file.txt"  # 自动拼接
p.exists()
p.mkdir(parents=True, exist_ok=True)