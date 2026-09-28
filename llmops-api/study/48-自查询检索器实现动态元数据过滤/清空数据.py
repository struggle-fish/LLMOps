"""
@Time   : 2026/9/27 20:42
@Author : jzy
@File   : 清空数据.py
"""

import os
import dotenv
from pinecone import Pinecone

dotenv.load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("llmops")

# 删除dataset命名空间下全部向量！！！
index.delete(delete_all=True, namespace="dataset")
print("dataset命名空间全部数据已清空")
