"""
@Time   : 2026/8/28 13:53
@Author : jzy
@File   : 2.configurable_fields使用.py
"""
import os

import dotenv

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import ConfigurableField

dotenv.load_dotenv()

prompt = PromptTemplate.from_template("请生成一个小于{x}的随机数")

llm = ChatOpenAI(model=os.getenv('OPENAI_MODEL')).configurable_fields(
    temperature=ConfigurableField(
        id="llm_temperature",
        name="大语言模型的温度",
        description="温度越低，大语言模型生成的内容越确定，温度越高生成内容越随机"
    )
)

chain = prompt | llm | StrOutputParser()

content = chain.invoke({"x": 1000})
print(content)
print("==================")

# 将temperature修改为0调用内容
content = chain.invoke(
    {"x", 1000},
    config={"configurable": {"llm_temperature": 0}}
)

print(content)
