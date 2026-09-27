"""
@Time   : 2026/9/23 15:05
@Author : jzy
@File   : 1.语义分割器使用示例.py.py
"""
import dotenv
from langchain_unstructured import UnstructuredLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

dotenv.load_dotenv()

# 1.构建加载器和文本分割器
loader = UnstructuredLoader(file_path="./科幻短篇.txt")
text_splitter = SemanticChunker(
    embeddings=OpenAIEmbeddings(model="text-embedding-3-small"),
    # number_of_chunks=10,  # ❌删掉，SemanticChunker不支持这个参数
    add_start_index=True,
    sentence_split_regex=r"(?<=[。？！.?!])",
    # 可选：调整语义断点阈值，数值越大块越少
    # breakpoint_threshold_amount=0.7
)
# 2.加载文本与分割
documents = loader.load()
chunks = text_splitter.split_documents(documents)
# 3.循环打印
for chunk in chunks:
    print(f"块大小: {len(chunk.page_content)}, 元数据: {chunk.metadata}")

print(f"\n一共分割出 {len(chunks)} 个块")
