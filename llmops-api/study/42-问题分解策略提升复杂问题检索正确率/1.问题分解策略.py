"""
@Time   : 2026/9/26 22:07
@Author : jzy
@File   : 1.问题分解策略.py
"""
import os
from operator import itemgetter

import dotenv
import weaviate

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_weaviate import WeaviateVectorStore
from weaviate.auth import AuthApiKey
from weaviate.config import AdditionalConfig, Timeout

dotenv.load_dotenv()

# 读取环境变量
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

# ========== LangSmith追踪配置（新增这一段，上报trace） ==========
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_PROJECT"] = "LLMOpsDev"


# =================================================================

def format_qa_pair(question: str, answer: str) -> str:
    """格式化传递的问题+答案为单个字符串"""
    return f"Question: {question}\nAnswer: {answer}\n\n".strip()


# 1.定义分解子问题的prompt
decomposition_prompt = ChatPromptTemplate.from_template(
    "你是一个乐于助人的AI助理，可以针对一个输入问题生成多个相关的子问题。\n"
    "目标是将输入问题分解成一组可以独立回答的子问题或者子任务。\n"
    "生成与一下问题相关的多个搜索查询：{question}\n"
    "并使用换行符进行分割，输出（3个子问题/子查询）："
)

# 2.构建分解问题链
decomposition_chain = (
        {"question": RunnablePassthrough()}
        | decomposition_prompt
        | ChatOpenAI(model="gpt-5.4-mini", temperature=0)
        | StrOutputParser()
        | (lambda x: x.strip().split("\n"))
)

# 1. 建立Weaviate连接（沿用之前可用配置，跳过gRPC健康检查）
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_URL,
    auth_credentials=AuthApiKey(WEAVIATE_API_KEY),
    additional_config=AdditionalConfig(
        timeout=Timeout(init=30, query=60, insert=120)
    ),
    skip_init_checks=True
)

# 2. 构建向量库
embedding = OpenAIEmbeddings(model="text-embedding-3-small")
db = WeaviateVectorStore(
    client=client,
    index_name="DatasetDemo",
    text_key="text",
    embedding=embedding
)

retriever = db.as_retriever(search_type="mmr")

# 4.执行提问获取子问题
question = "关于LLMOps应用配置的文档有哪些"
sub_questions = decomposition_chain.invoke(question)

# 5.构建迭代问答链：提示模板+链
prompt = ChatPromptTemplate.from_template("""这是你需要回答的问题：
---
{question}
---

这是所有可用的背景问题和答案对：
---
{qa_pairs}
---

这是与问题相关的额外背景信息：
---
{context}
---""")

chain = (
        {
            "question": itemgetter("question"),
            "qa_pairs": itemgetter("qa_pairs"),
            "context": itemgetter("question") | retriever,
        }
        | prompt
        | ChatOpenAI(model="gpt-5.4-mini", temperature=0)
        | StrOutputParser()
)

# 5.循环遍历所有子问题进行检索并获取答案
qa_pairs = ""
for sub_question in sub_questions:
    answer = chain.invoke({"question": sub_question, "qa_pairs": qa_pairs})
    qa_pair = format_qa_pair(sub_question, answer)
    qa_pairs += "\n---\n" + qa_pair
    print("=" * 50)
    print(f"问题: {sub_question}")
    print(f"答案: {answer}")

client.close()
