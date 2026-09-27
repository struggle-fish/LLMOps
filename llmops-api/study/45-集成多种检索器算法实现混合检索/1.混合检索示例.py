"""
@Time   : 2026/9/27 09:57
@Author : jzy
@File   : 1.混合检索示例.py
"""
""" @Time   : 2026/9/27 09:57 @Author : jzy @File   : 1.混合检索示例.py """
import os
import dotenv
import weaviate
from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_weaviate import WeaviateVectorStore
from weaviate.auth import AuthApiKey
from weaviate.config import AdditionalConfig, Timeout

dotenv.load_dotenv()

# 读取环境变量
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

# ========== LangSmith追踪配置 ==========
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_PROJECT"] = "LLMOpsDev"

# 1.创建文档列表
documents = [
    Document(page_content="笨笨是一只很喜欢睡觉的猫咪", metadata={"page": 1}),
    Document(page_content="我喜欢在夜晚听音乐，这让我感到放松。", metadata={"page": 2}),
    Document(page_content="猫咪在窗台上打盹，看起来非常可爱。", metadata={"page": 3}),
    Document(page_content="学习新技能是每个人都应该追求的目标。", metadata={"page": 4}),
    Document(page_content="我最喜欢的食物是意大利面，尤其是番茄酱的那种。", metadata={"page": 5}),
    Document(page_content="昨晚我做了一个奇怪的梦，梦见自己在太空飞行。", metadata={"page": 6}),
    Document(page_content="我的手机突然关机了，让我有些焦虑。", metadata={"page": 7}),
    Document(page_content="阅读是我每天都会做的事情，我觉得很充实。", metadata={"page": 8}),
    Document(page_content="他们一起计划了一次周末的野餐，希望天气能好。", metadata={"page": 9}),
    Document(page_content="我的狗喜欢追逐球，看起来非常开心。", metadata={"page": 10}),
]

# 2.构建BM25关键词检索器（本地稀疏检索）
bm25_retriever = BM25Retriever.from_documents(documents)
bm25_retriever.k = 4

# 3.连接Weaviate向量库
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_URL,
    auth_credentials=AuthApiKey(WEAVIATE_API_KEY),
    additional_config=AdditionalConfig(
        timeout=Timeout(init=30, query=60, insert=120)
    ),
    skip_init_checks=True
)

try:
    embedding = OpenAIEmbeddings(model="text-embedding-3-small")
    # 写入文档到Weaviate（如果之前DatasetDemo已经有这批数据，可以注释掉这行）
    db = WeaviateVectorStore.from_documents(
        documents,
        embedding,
        client=client,
        index_name="DatasetDemo",
        text_key="text")
    weaviate_retriever = db.as_retriever(search_kwargs={"k": 4})

    # 4.初始化集成检索器，RRF融合 BM25 + Weaviate向量检索
    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, weaviate_retriever],
        weights=[0.5, 0.5],
    )

    # 5.执行检索
    query = "除了猫，你养了什么宠物呢？"
    docs = ensemble_retriever.invoke(query)
    print(f"查询：{query}")
    print("==== 混合检索返回结果 ====")
    for doc in docs:
        print(f"content: {doc.page_content}, metadata: {doc.metadata}")
    print(f"\n检索到文档总数：{len(docs)}")

finally:
    client.close()
    print("\nWeaviate连接已关闭")
