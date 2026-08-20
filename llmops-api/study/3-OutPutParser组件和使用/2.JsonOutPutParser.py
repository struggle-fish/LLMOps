"""
@Time   : 2026/8/17 13:42
@Author : jzy
@File   : 2.JsonOutPutParser.py
"""

import dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from pydantic import BaseModel, Field

from langchain_core.output_parsers import PydanticOutputParser

dotenv.load_dotenv()


class Joke(BaseModel):
    joke: str = Field(description="回答用户的冷消化")

    punchline: str = Field(description="这个冷笑话的笑点")


# 实例化，传入 pydantic_object=Joke
parser = PydanticOutputParser(pydantic_object=Joke)

# 打印格式提示词
# print(parser.get_format_instructions())


# 构建一个提示模板
prompt = ChatPromptTemplate.from_template("请根据用户的提问进行回答.\n{format_instructions}\n{query}").partial(
    format_instructions=parser.get_format_instructions())

# print(prompt.format(query="请讲一个程序员的冷笑话"))

# 构建一个大语言模型
llm = ChatOpenAI()

# 传递提示并解析
joke = parser.invoke(llm.invoke(prompt.invoke({"query": "请讲一个关于程序员的冷笑话"})))

print(joke)
