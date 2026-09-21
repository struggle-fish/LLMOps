"""
@Time   : 2026/9/18 14:52
@Author : jzy
@File   : 1.Document与TextLoader.py.py
"""

from langchain_community.document_loaders import TextLoader

# 1.构建加载器
loader = TextLoader("./电商产品数据.txt", encoding="utf-8")

# 2.加载数据

documents = loader.load()

print("文档数量:", len(documents))
print("文档内容:", documents[0].metadata)
