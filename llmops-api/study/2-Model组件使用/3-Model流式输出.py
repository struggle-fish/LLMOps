"""
@Time   : 2026/8/17 10:07
@Author : jzy
@File   : 3-Model流式输出.py
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
response = ai_messages = llm.stream(prompt.invoke(
    {"subject": "能简单介绍下LLM和LLMOps吗"}
))

for chunk in response:
    print(chunk.content, flush=True, end="")
