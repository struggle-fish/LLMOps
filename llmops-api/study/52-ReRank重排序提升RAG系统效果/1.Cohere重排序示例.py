"""
@Time   : 2026/9/28 10:10
@Author : jzy
@File   : 1.Cohere重排序示例.py
"""
import os

import dotenv
import weaviate
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from langchain_openai import OpenAIEmbeddings
from langchain_weaviate import WeaviateVectorStore
from weaviate.auth import AuthApiKey
from weaviate.config import AdditionalConfig, Timeout

dotenv.load_dotenv()
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")
# 1.创建向量数据库与重排组件
embedding = OpenAIEmbeddings(model="text-embedding-3-small")

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_URL,
    auth_credentials=AuthApiKey(WEAVIATE_API_KEY),
    additional_config=AdditionalConfig(
        timeout=Timeout(init=30, query=60, insert=120)
    ),
    skip_init_checks=True
)

db = WeaviateVectorStore(
    client=client,
    index_name="ParentDocument",
    text_key="text",
    embedding=embedding,
)

rerank = CohereRerank(model="rerank-multilingual-v3.0")

# 2.构建压缩检索器
retriever = ContextualCompressionRetriever(
    base_retriever=db.as_retriever(search_type="mmr"),
    base_compressor=rerank,
)

# 3.执行搜索并排序
search_docs = retriever.invoke("关于LLMOps应用配置的信息有哪些呢？")
print(search_docs)
print(len(search_docs))
client.close()
