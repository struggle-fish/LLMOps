"""
@Time   : 2026/9/27 21:34
@Author : jzy
@File   : 1.父文档检索器示例.py
"""
import os

import dotenv
import weaviate
from langchain_classic.retrievers import ParentDocumentRetriever
from langchain_classic.storage import LocalFileStore

from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_weaviate import WeaviateVectorStore
from weaviate.auth import AuthApiKey
from weaviate.config import AdditionalConfig, Timeout

dotenv.load_dotenv()
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")
# 1.创建加载器与文档列表，并加载文档
loaders = [
    UnstructuredFileLoader("./电商产品数据.txt"),
    UnstructuredFileLoader("./项目API文档.md"),
]

docs = []
for loader in loaders:
    docs.extend(loader.load())

# 2.创建文本分割器
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)

# 3.创建向量数据库与文档数据库

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_URL,
    auth_credentials=AuthApiKey(WEAVIATE_API_KEY),
    additional_config=AdditionalConfig(
        timeout=Timeout(init=30, query=60, insert=120)
    ),
    skip_init_checks=True
)

embedding = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = WeaviateVectorStore(
    client=client,
    index_name="ParentDocument",
    text_key="text",
    embedding=embedding,
)

byte_store = LocalFileStore("./parent-document")

# 4.创建父文档检索器
retriever = ParentDocumentRetriever(
    vectorstore=vector_store,
    byte_store=byte_store,
    child_splitter=text_splitter,
)

# 5.添加文档
# retriever.add_documents(docs, ids=None)

# 6.检索并返回内容
search_docs = retriever.vectorstore.similarity_search("分享关于LLMOps的一些应用配置")
# search_docs = retriever.invoke("分享关于LLMOps的一些应用配置")
print(search_docs)
print(len(search_docs))
client.close()
