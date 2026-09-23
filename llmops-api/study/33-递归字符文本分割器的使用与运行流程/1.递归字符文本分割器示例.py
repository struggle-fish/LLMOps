"""
@Time   : 2026/9/22 15:16
@Author : jzy
@File   : 1.递归字符文本分割器示例.py.py
"""
from langchain_unstructured import UnstructuredLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 替换原来 UnstructuredMarkdownLoader，file_path传文件路径
loader = UnstructuredLoader(file_path="./项目API文档.md", partition_via_api=False)
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    add_start_index=True,
)
chunks = text_splitter.split_documents(documents)

for chunk in chunks:
    print(f"块大小: {len(chunk.page_content)}, 元数据: {chunk.metadata}")
