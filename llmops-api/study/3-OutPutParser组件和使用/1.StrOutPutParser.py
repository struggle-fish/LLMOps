"""
@Time   : 2026/8/17 13:23
@Author : jzy
@File   : 1.StrOutPutParser.py
"""
import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

dotenv.load_dotenv()

# 提示词模板
prompt = ChatPromptTemplate.from_template("{query}")

# 构建大语言模型
llm = ChatOpenAI()

# 创建字符串输出解析器
parser = StrOutputParser()

content = parser.invoke(llm.invoke(prompt.invoke({"query": "你好你是"})))

print(content)
