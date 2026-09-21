"""
@Time   : 2026/9/17 15:37
@Author : jzy
@File   : 2.带过滤的相似性.py
"""
import dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

dotenv.load_dotenv()

embedding = OpenAIEmbeddings(model="text-embedding-3-small")

db = PineconeVectorStore(
    index_name="llmops",
    embedding=embedding,
    namespace="dataset")

id = "be899f44-9326-4283-9955-297cdad02564"

db.delete([id], namespace="dataset")
