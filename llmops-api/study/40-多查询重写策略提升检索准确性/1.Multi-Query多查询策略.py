""" @Time   : 2026/9/26 13:48 @Author : jzy @File   : 1.Multi-Query多查询策略.py """
import os
import dotenv
import weaviate
from weaviate.auth import AuthApiKey
from weaviate.config import AdditionalConfig, Timeout
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_weaviate import WeaviateVectorStore

dotenv.load_dotenv()

# 读取环境变量
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

# ========== LangSmith追踪配置（新增这一段，上报trace） ==========
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_PROJECT"] = "LLMOpsDev"
# =================================================================

# 1. 建立Weaviate连接（沿用之前可用配置，跳过gRPC健康检查）
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_URL,
    auth_credentials=AuthApiKey(WEAVIATE_API_KEY),
    additional_config=AdditionalConfig(
        timeout=Timeout(init=30, query=60, insert=120)
    ),
    skip_init_checks=True
)

# 2. 构建向量库
embedding = OpenAIEmbeddings(model="text-embedding-3-small")
db = WeaviateVectorStore(
    client=client,
    index_name="DatasetDemo",
    text_key="text",
    embedding=embedding
)

# 基础检索器：MMR 多样性检索，k=3
retriever = db.as_retriever(search_type="mmr", search_kwargs={"k": 3})

# 3. 创建多查询检索器：LLM自动改写生成多个子问题，扩大召回
llm = ChatOpenAI(model="gpt-5.4-mini", temperature=0)
multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=retriever,
    llm=llm,
    include_original=True,  # 把原始查询也加入检索集合
)

# 4. 执行检索
query = "关于LLMOps应用配置的文档有哪些"
docs = multi_query_retriever.invoke(query)

# ========== 美化打印输出 ==========
print("=" * 50)
print(f"原始用户问题：{query}")
print(f"\n检索到文档总数：{len(docs)}")
print("=" * 50)
for idx, doc in enumerate(docs):
    print(f"\n【文档 {idx + 1}】")
    print(f"内容：{doc.page_content}")
    print(f"元数据：{doc.metadata}")

client.close()
