"""
@Time   : 2026/9/26 20:45
@Author : jzy
@File   : 1.RAG多查询结果融合策略.py.py
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/7/3 23:45
@Author  : thezehui@gmail.com
@File    : 1.RAG多查询结果融合策略.py
"""
from typing import List
import os
import dotenv
import weaviate
from weaviate.auth import AuthApiKey
from weaviate.config import AdditionalConfig, Timeout
from langchain_core.load import dumps, loads
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_weaviate import WeaviateVectorStore

dotenv.load_dotenv()

# ========= LangSmith追踪配置 =========
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_PROJECT"] = "LLMOpsDev"
# =====================================


WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")


class RAGFusionRetriever(MultiQueryRetriever):
    """RAG多查询结果融合策略检索器"""
    k: int = 4

    def retrieve_documents(
            self, queries: List[str], run_manager: CallbackManagerForRetrieverRun
    ) -> List[List[Document]]:
        """重写检索文档函数，返回值变成一个嵌套的列表"""
        documents = []
        for query in queries:
            docs = self.retriever.invoke(
                query, config={"callbacks": run_manager.get_child()}
            )
            documents.append(docs)
        return documents

    def unique_union(self, documents: List[List[Document]]) -> List[Document]:
        """使用RRF算法来去重合并对应的文档，参数为嵌套列表，返回值为文档列表"""
        # 1.定义一个变量存储每个文档的得分信息
        fused_result = {}
        # 2.循环两层获取每一个文档信息
        for docs in documents:
            for rank, doc in enumerate(docs):
                # 3.使用dumps函数将类示例转换成字符串
                doc_str = dumps(doc)
                # 4.判断下该文档的字符串是否已经计算过得分
                if doc_str not in fused_result:
                    fused_result[doc_str] = 0
                # 5.RRF公式：1/(rank+60)
                fused_result[doc_str] += 1 / (rank + 60)
        # 6.执行排序操作，获取相应的数据，使用的是降序
        reranked_results = [
            (loads(doc), score)
            for doc, score in sorted(fused_result.items(), key=lambda x: x[1], reverse=True)
        ]
        return [item[0] for item in reranked_results[:self.k]]


# 1.构建向量数据库与检索器
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_URL,
    auth_credentials=AuthApiKey(WEAVIATE_API_KEY),
    additional_config=AdditionalConfig(
        timeout=Timeout(init=30, query=60, insert=120)
    ),
    skip_init_checks=True
)

embedding = OpenAIEmbeddings(model="text-embedding-3-small")
db = WeaviateVectorStore(
    client=client,
    index_name="DatasetDemo",
    text_key="text",
    embedding=embedding,
)
retriever = db.as_retriever(search_type="mmr", search_kwargs={"k": 3})

rag_fusion_retriever = RAGFusionRetriever.from_llm(
    retriever=retriever,
    llm=ChatOpenAI(model="gpt-5.4-mini", temperature=0),
)

# 3.执行检索
query = "关于LLMOps应用配置的文档有哪些"
docs = rag_fusion_retriever.invoke(query)

print("=" * 50)
print(docs)
print(len(docs))

client.close()
