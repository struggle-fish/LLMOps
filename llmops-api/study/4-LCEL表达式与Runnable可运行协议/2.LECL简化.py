"""
@Time   : 2026/8/17 19:59
@Author : jzy
@File   : 2.LECL简化.py
"""
from typing import Any

import dotenv

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

# 构建组件
prompt = ChatPromptTemplate.from_template("{query}")

llm = ChatOpenAI()

parser = StrOutputParser()

chain = prompt | llm | parser

print(chain.invoke({"query": "请讲一个程序员的冷笑话"}))
