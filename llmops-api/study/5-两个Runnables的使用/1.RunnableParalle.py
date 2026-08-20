"""
@Time   : 2026/8/18 13:07
@Author : jzy
@File   : 1.RunnableParalle.py
"""

import dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

dotenv.load_dotenv()

# prompt
joke_prompt = ChatPromptTemplate.from_template("请讲一个关于{subject}的冷笑话，尽可能短一些")
poem_prompt = ChatPromptTemplate.from_template("请写一篇关于{subject}的诗,尽可能短一些")

# 创建语言模型
llm = ChatOpenAI()

# 创建输出解析器
parser = StrOutputParser()

# 编排链
joke_chain = joke_prompt | llm | parser

poem_chain = poem_prompt | llm | parser

# 并行链
map_chain = RunnableParallel({
    "joke": joke_chain,
    "poem": poem_chain
})

res = map_chain.invoke({"subject": "程序员"})

print(res)
