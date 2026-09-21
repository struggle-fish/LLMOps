"""
@Time   : 2026/9/21 17:30
@Author : jzy
@File   : 4.通用文件加载器.py.py
"""
from langchain_unstructured import UnstructuredLoader

loader = UnstructuredLoader("./项目API资料.md")
documents = loader.load()

print(documents)
print(len(documents))
print(documents[0].metadata)
