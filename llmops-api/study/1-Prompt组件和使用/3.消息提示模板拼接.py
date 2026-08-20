"""
@Time   : 2026/8/13 15:39
@Author : jzy
@File   : 3.消息提示模板拼接.py
"""

from langchain_core.prompts import ChatPromptTemplate

system_chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个有趣的笑话生成器,当前时间是{now}"),
])

human_chat_prompt = ChatPromptTemplate.from_messages([
    ("human", "{query}"),
])

chat_prompt = system_chat_prompt + human_chat_prompt

print(chat_prompt.invoke({
    "now": "2026-08-13 15:39",
    "query": "请讲一个关于程序员的冷笑话"
}).to_string())
