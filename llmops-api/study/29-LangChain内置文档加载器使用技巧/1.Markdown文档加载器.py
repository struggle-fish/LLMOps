"""
@Time   : 2026/9/18 16:08
@Author : jzy
@File   : 1.Markdown文档加载器.py.py
"""

from langchain_unstructured import UnstructuredLoader

loader = UnstructuredLoader("./项目API资料.md")
documents = loader.load()

print(documents)
print(len(documents))
print(documents[0].metadata)
