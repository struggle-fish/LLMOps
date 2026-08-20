"""
@Time   : 2026/8/18 13:22
@Author : jzy
@File   : 2.RunnableParallel模拟检索.py
"""
from operator import itemgetter

import dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

dotenv.load_dotenv()


# 模拟检索
def retrieval(query: str) -> str:
    """模拟检索器"""
    print("正在检索中。。。")
    return "我是小铜钱"


# prompt
prompt = ChatPromptTemplate.from_template("""
    请根据用户的问题回答，可以参考对应的上下文进行生成
    
    <context>
    {context}
    </context>
    用户的提问是：{query}


""")

# 构建大语言模型

llm = ChatOpenAI()

# 输出解析器
parser = StrOutputParser()

# 构建链
"""
chain = RunnableParallel({
    "context": lambda x: retrieval(x["query"]),
    # "query": lambda x: x["query"]
    "query": itemgetter("query")
}) | prompt | llm | parser

"""
chain = {
            "context": lambda x: retrieval(x["query"]),
            "query": itemgetter("query")
        } | prompt | llm | parser

# 调用链
content = chain.invoke({
    "query": "你好，我是谁？"
})

print(content)
