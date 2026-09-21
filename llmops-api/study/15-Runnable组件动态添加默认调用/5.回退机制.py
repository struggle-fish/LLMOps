"""
@Time   : 2026/8/29 15:21
@Author : jzy
@File   : 5.回退机制.py
"""
import os

import dotenv
from langchain_community.chat_models import QianfanChatEndpoint

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import ConfigurableField
from langchain_community.chat_models.baidu_qianfan_endpoint import QianfanChatEndpoint

dotenv.load_dotenv()

prompt = ChatPromptTemplate.from_template("{query}")

llm = ChatOpenAI(model='gpt-3.5-turbo-18k').with_fallbacks([QianfanChatEndpoint()])

chain = prompt | llm.bind(stop="world") | StrOutputParser()

content = chain.invoke(
    {"query", "你好你是什么模型"},
    config={"configurable": {"llm": "wenxin"}}
)

print(content)
