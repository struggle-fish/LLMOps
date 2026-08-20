"""
@Time   : 2026/8/13 15:35
@Author : jzy
@File   : 2.字符串提示拼接.py
"""
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template("请讲一个关于{subject}的冷笑话") + "让我开心下"

print(prompt.invoke({"subject": "程序员"}).to_string())
