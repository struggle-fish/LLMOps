"""
@Time   : 2026/8/17 09:59
@Author : jzy
@File   : 2-Model批处理.py
"""
from datetime import datetime

import dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

# 提示词
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个有趣的笑话生成器,当前时间是{now}"),
    ("human", "{subject}")

]).partial(now=datetime.now())

# 创建大语言模型
llm = ChatOpenAI()

# 批次处理
ai_messages = llm.batch([
    prompt.invoke({"subject": "你好你是"}),
    prompt.invoke({"subject": "请讲一个程序员的冷笑话"})
])

for ai_message in ai_messages:
    print(ai_message.content)
    print("===============")
