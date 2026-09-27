"""
@Time   : 2026/9/26 21:15
@Author : jzy
@File   : 把项目API文档作为数据存储.py
"""
import dotenv
import os
import weaviate
from langchain_weaviate import WeaviateVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
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

# ========== 新增：读取本地 Markdown 文件 ==========
md_file_path = "./项目API文档.md"
with open(md_file_path, "r", encoding="utf-8") as f:
    md_content = f.read()

# 文档切分器，按markdown换行、段落切割
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=80,
    separators=["\n\n", "\n", "##", "###", "#"]
)
chunks = text_splitter.split_text(md_content)

# 构造Document列表，统一加元数据
documents = []
for idx, chunk in enumerate(chunks):
    documents.append(Document(
        page_content=chunk,
        metadata={"source": "项目API文档.md", "chunk_id": idx}
    ))
# ================================================

embedding = OpenAIEmbeddings(model="text-embedding-3-small")
# 绑定集合名称 DatasetDemo
db = WeaviateVectorStore(
    client=client,
    index_name="DatasetDemo",
    text_key="text",
    embedding=embedding
)

# 写入分片后的文档
ids = db.add_documents(documents)
print(f"成功上传 {len(ids)} 条分片到Weaviate DatasetDemo")

# 测试检索
retriever = db.as_retriever()
res = retriever.invoke("接口")
for doc in res:
    print("======")
    print(doc.page_content)

client.close()
