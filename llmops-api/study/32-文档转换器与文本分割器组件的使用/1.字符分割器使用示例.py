"""
@Time   : 2026/9/22 14:46
@Author : jzy
@File   : 1.字符分割器使用示例.py.py
"""
from langchain_unstructured import UnstructuredLoader
from langchain_text_splitters import CharacterTextSplitter

# 1.加载md文档，新版独立包的Loader，不再来自 langchain_community
loader = UnstructuredLoader(file_path="./项目API文档.md")
documents = loader.load()

# 2.创建文本分割器（完全不变）
text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=500,
    chunk_overlap=50,
    add_start_index=True,
)

# 3.分割文本
chunks = text_splitter.split_documents(documents)

for chunk in chunks:
    print(f"块大小:{len(chunk.page_content)}, 元数据:{chunk.metadata}")

print(len(chunks))
