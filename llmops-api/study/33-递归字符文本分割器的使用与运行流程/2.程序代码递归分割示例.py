"""
@Time   : 2026/9/23 14:48
@Author : jzy
@File   : 2.程序代码递归分割示例.py.py
"""
from langchain_unstructured import UnstructuredLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language

loader = UnstructuredLoader(file_path="demo.py")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=500,
    chunk_overlap=50,
    add_start_index=True,
)
chunks = text_splitter.split_documents(documents)

for chunk in chunks:
    print(f"块大小: {len(chunk.page_content)}, 元数据: {chunk.metadata}")

print(chunks[2].page_content)
