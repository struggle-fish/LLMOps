"""
@Time   : 2026/9/22 13:55
@Author : jzy
@File   : 2.FileSystemBlobLoader示例.py.py
"""
from langchain_community.document_loaders.blob_loaders import FileSystemBlobLoader

loader = FileSystemBlobLoader(".", show_progress=True)

for blob in loader.yield_blobs():
    print(blob.as_string())
