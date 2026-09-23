"""
@Time   : 2026/9/23 15:00
@Author : jzy
@File   : 3.分割中英文场景示例.py.py
"""
from langchain_unstructured import UnstructuredLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 替换原来 UnstructuredMarkdownLoader，file_path传文件路径
loader = UnstructuredLoader(file_path="./项目API文档.md", partition_via_api=False)

separators = [
    "\n\n",
    "\n",
    "。|！|？",
    "\.\s|\!\s|\?\s",  # 英文标点符号后面通常需要加空格
    "；|;\s",
    "，|,\s",
    " ",
    ""
]

text_splitter = RecursiveCharacterTextSplitter(
    separators=separators,
    is_separator_regex=True,
    chunk_size=500,
    chunk_overlap=50,
    add_start_index=True,
)

documents = loader.load()
chunks = text_splitter.split_documents(documents)

for chunk in chunks:
    print(f"块大小: {len(chunk.page_content)}, 元数据: {chunk.metadata}")
