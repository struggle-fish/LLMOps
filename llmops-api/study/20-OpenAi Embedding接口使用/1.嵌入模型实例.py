"""
@Time   : 2026/8/30 19:36
@Author : jzy
@File   : 1.嵌入模型实例.py
"""
import os

import dotenv
import numpy as np

from langchain_openai import OpenAIEmbeddings

from numpy.linalg import norm

dotenv.load_dotenv()


def cosine_similarity(vec1: list, vec2: list) -> float:
    """计算两个向量的余弦相似度"""
    # 计算两个向量的点击
    dot_product = np.dot(vec1, vec2)
    # 计算向量的长度
    vec1_norm = norm(vec1)
    vec2_norm = norm(vec2)
    # 计算余弦相似度
    return dot_product / (vec1_norm * vec2_norm)


# 中转站可能不支持这个模型
# 创建文本嵌入模型
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
)

# 嵌入文本
query_vector = embeddings.embed_query('我叫小铜钱，我喜欢打篮球')
print(query_vector)
print(len(query_vector))

# 嵌入文档列表、字符串列表
documents_vector = embeddings.embed_documents([
    "我叫小铜钱，喜欢打篮球",
    "这个喜欢打篮球的人叫小铜钱",
    "求知若渴，虚心若愚"
])

# 计算余弦相似度
print("向量1和向量2的相似度", cosine_similarity(documents_vector[0], documents_vector[1]))
print("向量1和向量3的相似度", cosine_similarity(documents_vector[0], documents_vector[2]))
