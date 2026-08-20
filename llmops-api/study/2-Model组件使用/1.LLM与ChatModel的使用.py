"""
@Time   : 2026/8/14 11:06
@Author : jzy
@File   : 1.LLM与ChatModel的使用.py
"""
from datetime import datetime

import dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

# 提示词
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个有趣的笑话生成器,当前时间是{now}"),
    ("human", "请讲一个关于{subject}的冷笑话")

]).partial(now=datetime.now())

# 创建大语言模型
llm = ChatOpenAI()

ai_message = llm.invoke(prompt.invoke(
    {
        "subject": "程序员"
    }
))

print(ai_message.content)
