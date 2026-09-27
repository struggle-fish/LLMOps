"""
@Time   : 2026/9/27 17:26
@Author : jzy
@File   : 1.函数回调规范化输出.py
"""
""" @Time   : 2026/9/27 17:26 @Author : jzy @File   : 1.函数回调规范化输出.py """
from typing import Literal
import dotenv
from pydantic.v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()


class RouteQuery(BaseModel):
    """将用户查询映射到对应的数据源上"""
    datasource: Literal["python_docs", "js_docs", "golang_docs"] = Field(
        description="根据用户的问题，选择哪个数据源最相关以回答用户的问题"
    )


# 1.创建绑定结构化输出的大语言模型，修正模型名称
llm = ChatOpenAI(model="gpt-5.4-mini", temperature=0)
structured_llm = llm.with_structured_output(RouteQuery)

# ========== 关键：增加系统提示词，告诉模型路由规则 ==========
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个查询路由专家。你的任务是将用户问题路由到对应的知识库：
- python_docs：Python编程语言相关问题
- js_docs：JavaScript / JS 编程语言相关问题
- golang_docs：Golang编程语言相关问题
只需要输出对应的 datasource，不要多余内容。"""),
    ("human", "{question}")
])

# 把prompt和结构化模型拼接成可调用链
router_chain = prompt | structured_llm

# 2.构建一个问题
question = """为什么下面的代码不工作了，请帮我检查下：
var a = "123" """

res: RouteQuery = router_chain.invoke({"question": question})

print(res)
print(type(res))
print(res.datasource)
