"""
@Time   : 2026/8/28 18:03
@Author : jzy
@File   : 4.动态替换运行组件.py
"""
import os

import dotenv
from langchain_community.chat_models import QianfanChatEndpoint

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import ConfigurableField

dotenv.load_dotenv()

prompt = ChatPromptTemplate.from_template("{query}")

llm = ChatOpenAI(model=os.getenv('OPENAI_MODEL')).configurable_alternatives(
    ConfigurableField(id="llm"),
    default_key="gpt-5.4-mini",
    wenxin=QianfanChatEndpoint()
)

chain = prompt | llm.bind(stop="world") | StrOutputParser()

content = chain.invoke(
    {"query", "你好你是什么模型"},
    config={"configurable": {"llm": "wenxin"}}
)

print(content)
