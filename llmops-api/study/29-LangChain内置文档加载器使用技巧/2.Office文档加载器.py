"""
@Time   : 2026/9/21 16:41
@Author : jzy
@File   : 2.Office文档加载器.py.py
"""
from langchain_unstructured import UnstructuredLoader

# 不管md/pptx/xlsx/docx，全部用这一个类
excel_loader = UnstructuredLoader(file_path="./员工考勤表.xlsx")
documents = excel_loader.load()

print(documents)
print(len(documents))
print(documents[0].metadata)
