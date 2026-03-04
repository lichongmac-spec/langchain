# DeepSeek 模型服务使用说明

本项目提供了一个封装良好的DeepSeek模型服务，方便在项目内其他文件中调用。

## 功能特性

- 统一的DeepSeek模型服务接口
- 支持基本调用、流式调用和事件流
- 配置管理和环境变量支持
- 与项目内其他服务（如MiniMax服务）保持一致的接口风格
- 提供同步包装的事件流接口，方便在同步代码中使用

## 安装要求

1. Python 3.13
2. DeepSeek API 密钥
3. 依赖包：`langchain_deepseek`, `python-dotenv`

## 安装步骤

### 1. 安装依赖包

由于Homebrew管理的Python 3.13遵循PEP 668限制，推荐使用虚拟环境安装：

```bash
# 创建虚拟环境
python3.13 -m venv .venv

# 激活虚拟环境
source .venv/bin/activate

# 安装依赖
pip install langchain_deepseek python-dotenv
```

或者使用以下命令绕过PEP 668限制（不推荐在生产环境使用）：

```bash
python3.13 -m pip install langchain_deepseek python-dotenv --break-system-packages
```

### 2. 配置API密钥

在项目根目录创建`.env`文件，并添加DeepSeek API密钥：

```bash
touch .env
```

在`.env`文件中添加：

```
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_MODEL_NAME=deepseek-chat  # 可选，默认使用deepseek-chat
```

## 使用方法

### 基本使用

```python
# 导入服务
from deepseek_service import invoke_deepseek

# 进行基本调用
response = invoke_deepseek("你好")
print(response.content)
```

### 获取LLM实例

```python
# 导入服务
from deepseek_service import get_deepseek_llm

# 获取LLM实例
llm = get_deepseek_llm()

# 使用LLM实例进行调用
response = llm.invoke("你好")
print(response.content)
```

### 流式调用

```python
# 导入服务
from deepseek_service import stream_deepseek

# 进行流式调用
full = None
for chunk in stream_deepseek("What color is the sky?"):
    full = chunk if full is None else full + chunk
    print(full.content, end="\r")
print()
```

### 消息列表调用

```python
# 导入服务
from deepseek_service import invoke_deepseek

# 消息列表
messages = [
    ("system", "You are a helpful assistant that translates English to French."),
    ("human", "I love programming."),
]

# 进行调用
response = invoke_deepseek(messages)
print(response.content)
```

### 自定义服务实例

```python
# 导入服务
from deepseek_service import DeepSeekService

# 创建自定义服务实例
custom_service = DeepSeekService(
    model_name="deepseek-chat",
    temperature=0.9,
    max_retries=3
)

# 获取LLM实例
llm = custom_service.get_llm()

# 进行调用
response = llm.invoke("请列出5种常见的水果")
print(response.content)
```

### 事件流调用

```python
# 导入服务
from deepseek_service import sync_astream_events

# 使用事件流
for event in sync_astream_events("Hello"):
    if event["event"] == "on_chat_model_start":
        print(f"输入: {event['data']['input']}")
    elif event["event"] == "on_chat_model_stream":
        print(f"Token: {event['data']['chunk'].content}")
    elif event["event"] == "on_chat_model_end":
        print(f"完整消息: {event['data']['output'].content}")
```

## API 参考

### DeepSeekService 类

#### __init__(model_name=None, temperature=0.7, max_retries=2)
初始化DeepSeek服务

- `model_name`: 要使用的模型名称，默认从环境变量获取或使用"deepseek-chat"
- `temperature`: 生成文本的随机性（0.0-2.0），默认0.7
- `max_retries`: 最大重试次数，默认2

#### get_llm()
获取初始化的LLM实例

返回: `ChatDeepSeek` 实例

#### invoke(prompt, **kwargs)
直接调用模型生成响应

- `prompt`: 输入提示，可以是字符串或消息列表
- `**kwargs`: 其他传递给模型invoke方法的参数

返回: `AIMessage` 对象

#### stream(prompt, **kwargs)
流式调用模型生成响应

- `prompt`: 输入提示，可以是字符串或消息列表
- `**kwargs`: 其他传递给模型stream方法的参数

返回: 产生`AIMessageChunk`对象的生成器

#### astream_events(prompt, config=None, **kwargs)
异步流式获取模型生成事件

- `prompt`: 输入提示，可以是字符串或消息列表
- `config`: 运行配置
- `**kwargs`: 其他传递给模型astream_events方法的参数

返回: 产生事件字典的异步生成器

### 便捷函数

#### get_deepseek_llm()
获取默认的DeepSeek LLM实例

返回: `ChatDeepSeek` 实例

#### invoke_deepseek(prompt, **kwargs)
使用默认服务调用DeepSeek模型

- `prompt`: 输入提示，可以是字符串或消息列表
- `**kwargs`: 其他传递给模型invoke方法的参数

返回: `AIMessage` 对象

#### stream_deepseek(prompt, **kwargs)
使用默认服务流式调用DeepSeek模型

- `prompt`: 输入提示，可以是字符串或消息列表
- `**kwargs`: 其他传递给模型stream方法的参数

返回: 产生`AIMessageChunk`对象的生成器

#### astream_events_deepseek(prompt, config=None, **kwargs)
使用默认服务异步流式获取模型生成事件

- `prompt`: 输入提示，可以是字符串或消息列表
- `config`: 运行配置
- `**kwargs`: 其他传递给模型astream_events方法的参数

返回: 产生事件字典的异步生成器

#### sync_astream_events(prompt, model=None, config=None)
将异步事件流包装为同步迭代器

- `prompt`: 输入提示，可以是字符串或消息列表
- `model`: 模型实例，默认使用默认服务的模型
- `config`: 运行配置

返回: 产生事件字典的同步生成器

## 业务使用示例

请参考 `example_business_usage.py` 文件，该文件展示了如何在业务中使用这个DeepSeek服务：

```bash
python example_business_usage.py
```

## 示例代码

示例代码可以在以下文件中找到：

- `deepseekModel.py`: 服务的基本使用示例
- `example_business_usage.py`: 业务场景使用示例
- `deepseek_service.py`: 服务实现代码（包含更多示例）

## 与MiniMax服务的对比

DeepSeek服务与项目内的MiniMax服务保持一致的接口风格，便于在项目中统一使用：

| 功能 | DeepSeek服务 | MiniMax服务 |
|------|--------------|-------------|
| 基本调用 | invoke_deepseek() | invoke_minimax() |
| 获取LLM实例 | get_deepseek_llm() | get_minimax_llm() |
| 流式调用 | stream_deepseek() | 不支持 |
| 事件流 | sync_astream_events() | 不支持 |
| 自定义服务实例 | DeepSeekService | MiniMaxService |

## 注意事项

1. 确保正确配置API密钥，否则会抛出`ValueError`
2. 避免在生产环境中使用`--break-system-packages`参数
3. 流式调用和事件流功能需要支持异步的环境
4. 详细的错误处理请参考代码中的异常处理部分

## 故障排除

### ModuleNotFoundError: No module named 'langchain_deepseek'

确保已正确安装`langchain_deepseek`包，并且使用的Python环境与安装时的环境一致。

### ValueError: DEEPSEEK_API_KEY 必须在.env文件中设置

确保已在`.env`文件中正确设置了`DEEPSEEK_API_KEY`。

### 其他错误

请检查DeepSeek API密钥是否有效，网络连接是否正常，以及是否超过了API调用限制。

## 版本信息

- langchain_deepseek: 0.1.4
- Python: 3.13+

## 许可证

本项目遵循MIT许可证。