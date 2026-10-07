"""
@Time   : 2026/9/29 13:43
@Author : jzy
@File   : 1.DuckDuckGo搜索.py
"""
from langchain_community.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()

print(search.invoke("LangChain的最新版本是什么?"))
print("名字：", search.name)
print("描述：", search.description)
print("参数：", search.args)
print("是否直接返回：", search.return_direct)
