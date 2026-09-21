"""
@Time   : 2026/9/21 17:25
@Author : jzy
@File   : 3.URL网页加载器.py.py
"""
from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader(
    "https://imooc.com",
    header_template={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
)
documents = loader.load()

print(documents)
print(len(documents))
print(documents[0].metadata)
