import os
import numpy as np
from typing import List
from langchain_core.embeddings import Embeddings

# 确保环境变量设置
os.environ["TOKENIZERS_PARALLELISM"] = "false"

class MiniLMEmbeddings(Embeddings):
    """手动控制线程的embeddings实现"""
    def __init__(self):
        import torch
        from transformers import AutoTokenizer, AutoModel
        
        # 强制CPU并限制线程
        torch.set_num_threads(1)
        torch.set_num_interop_threads(1)
        
        # 加载模型
        self.tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
        self.model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
        self.model.eval()
        
    def _mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        import torch
        
        with torch.no_grad():
            encoded_input = self.tokenizer(texts, padding=True, truncation=True, return_tensors='pt', max_length=512)
            model_output = self.model(**encoded_input)
            embeddings = self._mean_pooling(model_output, encoded_input['attention_mask'])
            
            # 归一化
            embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
            return embeddings.tolist()
    
    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]

# 使用
embeddings = MiniLMEmbeddings()
vectorstore = DocArrayInMemorySearch.from_texts(
    ["harrison worked at kensho", "bears like to eat honey"],
    embedding=embeddings,
)