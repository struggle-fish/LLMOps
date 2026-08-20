"""
@Time   : 2026/8/12 13:19
@Author : jzy
@File   : 1.Prompt组件基础用法.py
"""
from datetime import datetime

from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

# prompt = PromptTemplate.from_template("请讲一个关于{subject}的冷笑话")
#
# print(prompt.format(subject="程序员"))
#
# prompt_value = prompt.invoke({"subject": "程序员1"})
# print(prompt_value.to_string())
# print(prompt_value.to_messages())

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个有趣的笑话生成器,当前时间是{now}"),
    MessagesPlaceholder("chat_history_messages"),
    HumanMessagePromptTemplate.from_template("请讲一个关于{subject}的冷笑话"),
]).partial(now=datetime.now())

chat_prompt_value = chat_prompt.invoke({
    "subject": "程序员",
    "chat_history_messages": [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "你好！有什么我可以帮你的吗？"}
    ]
})

print(chat_prompt_value)
print(chat_prompt_value.to_string())
