import sys
import os

# 设置Python路径，确保能够导入deepseek_service
sys.path.insert(0, '/Users/lichong/Documents/AI/langchain/langchain1.2')

# 导入DeepSeek服务
from deepseek_service import invoke_deepseek, stream_deepseek

# 业务示例：翻译服务
def translate_text(text, source_lang="English", target_lang="French"):
    """
    使用DeepSeek服务进行文本翻译
    
    参数:
        text (str): 要翻译的文本
        source_lang (str): 源语言
        target_lang (str): 目标语言
    
    返回:
        str: 翻译后的文本
    """
    prompt = f"将以下{source_lang}文本翻译成{target_lang}：\n{text}"
    response = invoke_deepseek(prompt)
    return response.content

# 业务示例：内容生成服务
def generate_content(topic, length="short"):
    """
    使用DeepSeek服务生成内容
    
    参数:
        topic (str): 生成内容的主题
        length (str): 内容长度 ("short", "medium", "long")
    
    返回:
        str: 生成的内容
    """
    length_prompt = "简洁" if length == "short" else "中等长度" if length == "medium" else "详细"
    prompt = f"请{length_prompt}介绍一下{topic}，内容要通俗易懂。"
    response = invoke_deepseek(prompt)
    return response.content

# 业务示例：流式内容生成
def generate_streaming_content(prompt):
    """
    使用DeepSeek服务进行流式内容生成
    
    参数:
        prompt (str): 生成内容的提示
    """
    print(f"生成内容: ")
    full_response = None
    for chunk in stream_deepseek(prompt):
        full_response = chunk if full_response is None else full_response + chunk
        print(full_response.content, end="\r")
    print()
    return full_response.content

# 主程序
def main():
    print("=== DeepSeek服务业务使用示例 ===")
    
    # 示例1：翻译服务
    print("\n1. 翻译服务示例")
    original_text = "I love programming."
    translated_text = translate_text(original_text)
    print(f"原文: {original_text}")
    print(f"翻译: {translated_text}")
    
    # 示例2：内容生成服务
    print("\n2. 内容生成服务示例")
    topic = "人工智能"
    content = generate_content(topic, length="medium")
    print(f"关于'{topic}'的介绍: {content}")
    
    # 示例3：流式内容生成
    print("\n3. 流式内容生成示例")
    streaming_prompt = "请解释什么是机器学习，并用一个简单的例子说明。"
    streaming_content = generate_streaming_content(streaming_prompt)
    
    print("\n=== 业务使用示例完成 ===")

if __name__ == "__main__":
    main()