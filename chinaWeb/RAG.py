# 需要安装：pip3 install rank-bm25

import os
import sys
import string
from rank_bm25 import BM25Okapi
from typing import List
import numpy as np

# 设置环境变量（虽然可能不需要，但保留）
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, project_root)

from minimax_service import get_minimax_llm
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, Runnable
from langchain_core.documents import Document

# 简单的BM25检索器实现，继承自Runnable
class SimpleBM25Retriever(Runnable):
    """基于BM25的简单检索器"""
    
    def tokenize(self, text: str) -> List[str]:
        """改进的分词方法，去除标点符号"""
        # 转换为小写并去除标点符号
        text = text.lower().translate(str.maketrans('', '', string.punctuation))
        return text.split()
    
    def __init__(self, texts: List[str]):
        self.texts = texts
        self.documents = [Document(page_content=t) for t in texts]
        # 使用改进的分词方法
        self.tokenized_corpus = [self.tokenize(doc.page_content) for doc in self.documents]
        self.bm25 = BM25Okapi(self.tokenized_corpus)
    
    def get_relevant_documents(self, query: str) -> List[Document]:
        """获取与查询相关的文档"""
        # 对查询进行分词
        tokenized_query = self.tokenize(query)
        # 获取BM25分数
        doc_scores = self.bm25.get_scores(tokenized_query)
        
        # 获取最相似的文档（这里取top 1）
        if len(doc_scores) > 0:
            best_idx = np.argmax(doc_scores)
            if doc_scores[best_idx] > 0:  # 只返回有匹配的
                return [self.documents[best_idx]]
        
        # BM25失败时，使用简单的关键词匹配作为后备
        query_lower = query.lower().translate(str.maketrans('', '', string.punctuation))
        for doc in self.documents:
            doc_lower = doc.page_content.lower().translate(str.maketrans('', '', string.punctuation))
            # 检查是否有任何查询词存在于文档中
            if any(word in doc_lower for word in tokenized_query):
                return [doc]
        
        return []
    
    def invoke(self, input: str, config=None, **kwargs) -> List[Document]:
        """实现Runnable接口的invoke方法"""
        return self.get_relevant_documents(input)

# 简单的向量存储模拟
class SimpleBM25VectorStore:
    """模拟向量存储的简单BM25实现"""
    
    def __init__(self, texts: List[str]):
        self.texts = texts
        self.retriever = SimpleBM25Retriever(texts)
    
    @classmethod
    def from_texts(cls, texts: List[str], embedding=None, **kwargs):
        """创建BM25向量存储"""
        return cls(texts)
    
    def as_retriever(self, **kwargs):
        """返回检索器"""
        return self.retriever
    
    def similarity_search(self, query: str, k: int = 1, **kwargs):
        """相似性搜索"""
        return self.retriever.get_relevant_documents(query)[:k]

print("正在初始化BM25检索器...")

try:
    # 使用BM25替代向量存储
    vectorstore = SimpleBM25VectorStore.from_texts(
        ["harrison worked at kensho", "bears like to eat honey"]
    )
    print("检索器创建成功！")
    
except Exception as e:
    print(f"错误详情: {e}")
    print(f"错误类型: {type(e)}")
    raise

retriever = vectorstore.as_retriever()

template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
model = get_minimax_llm()
output_parser = StrOutputParser()

setup_and_retrieval = RunnableParallel(
    {"context": retriever, "question": RunnablePassthrough()}
)
chain = setup_and_retrieval | prompt | model | output_parser

print("执行查询...")
result = chain.invoke("where did harrison work?")
print(f"结果: {result}")