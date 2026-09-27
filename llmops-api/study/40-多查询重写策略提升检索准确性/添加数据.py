""" @Time   : 2026/9/26 18:08 @Author : jzy @File   : 添加数据.py """
import dotenv
import os
import weaviate
from langchain_weaviate import WeaviateVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from weaviate.auth import AuthApiKey
from weaviate.config import AdditionalConfig, Timeout
from weaviate.classes.query import Filter

dotenv.load_dotenv()

# 读取环境变量
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

# 重点改动：增加超时，跳过gRPC初始化健康检查
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_URL,
    auth_credentials=AuthApiKey(WEAVIATE_API_KEY),
    additional_config=AdditionalConfig(
        timeout=Timeout(init=30, query=60, insert=120)
    ),
    skip_init_checks=True  # 跳过gRPC ping检查，解决国内网络gRPC超时
)

# 1.原始文本数据与元数据
texts = [
    "笨笨是一只很喜欢睡觉的猫咪",
    "我喜欢在夜晚听音乐，这让我感到放松。",
    "猫咪在窗台上打盹，看起来非常可爱。",
    "学习新技能是每个人都应该追求的目标。",
    "我最喜欢的食物是意大利面，尤其是番茄酱的那种。",
    "昨晚我做了一个奇怪的梦，梦见自己在太空飞行。",
    "我的手机突然关机了，让我有些焦虑。",
    "阅读是我每天都会做的事情，我觉得很充实。",
    "他们一起计划了一次周末的野餐，希望天气能好。",
    "我的狗喜欢追逐球，看起来非常开心。",
]
metadatas = [
    {"page": 1},
    {"page": 2},
    {"page": 3},
    {"page": 4},
    {"page": 5},
    {"page": 6, "account_id": 1},
    {"page": 7},
    {"page": 8},
    {"page": 9},
    {"page": 10},
]

embedding = OpenAIEmbeddings(model="text-embedding-3-small")
# 绑定集合名称 DatasetDemo
db = WeaviateVectorStore(
    client=client,
    index_name="DatasetDemo",
    text_key="text",
    embedding=embedding
)

# 插入数据
ids = db.add_texts(texts, metadatas)
print(ids)

# 5.执行相似性搜索
filters = Filter.by_property("page").greater_or_equal(5)
print(db.similarity_search_with_score("笨笨", filters=filters))
retriever = db.as_retriever()
print(retriever.invoke("笨笨"))

client.close()
