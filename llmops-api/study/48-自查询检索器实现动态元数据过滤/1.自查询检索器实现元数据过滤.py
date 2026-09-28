""" @Time   : 2026/9/27 19:59 @Author : jzy @File   : 1.自查询检索器实现元数据过滤.py """
import dotenv
import os
from langchain_classic.chains.query_constructor.base import AttributeInfo, load_query_constructor_runnable
from langchain_classic.retrievers.self_query.base import SelfQueryRetriever
from langchain_community.query_constructors.pinecone import PineconeTranslator
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

dotenv.load_dotenv()

# LangSmith安全写法，防止None报错
langsmith_api_key = os.getenv("LANGSMITH_API_KEY")
if langsmith_api_key:
    os.environ["LANGSMITH_TRACING"] = "true"
    os.environ["LANGSMITH_API_KEY"] = langsmith_api_key
    os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT", "LLMOpsDev")

# 1.构建文档列表
documents = [
    Document(
        page_content="肖申克的救赎",
        metadata={"year": 1994, "rating": 9.7, "director": "弗兰克·德拉邦特"},
    ),
    Document(
        page_content="霸王别姬",
        metadata={"year": 1993, "rating": 9.6, "director": "陈凯歌"},
    ),
    Document(
        page_content="阿甘正传",
        metadata={"year": 1994, "rating": 9.5, "director": "罗伯特·泽米吉斯"},
    ),
    Document(
        page_content="泰坦尼克号",
        metadata={"year": 1997, "rating": 9.5, "director": "詹姆斯·卡梅隆"},
    ),
    Document(
        page_content="千与千寻",
        metadata={"year": 2001, "rating": 9.4, "director": "宫崎骏"},
    ),
    Document(
        page_content="星际穿越",
        metadata={"year": 2014, "rating": 9.4, "director": "克里斯托弗·诺兰"},
    ),
    Document(
        page_content="忠犬八公的故事",
        metadata={"year": 2009, "rating": 9.4, "director": "莱塞·霍尔斯道姆"},
    ),
    Document(
        page_content="三傻大闹宝莱坞",
        metadata={"year": 2009, "rating": 9.2, "director": "拉库马·希拉尼"},
    ),
    Document(
        page_content="疯狂动物城",
        metadata={"year": 2016, "rating": 9.2, "director": "拜伦·霍华德"},
    ),
    Document(
        page_content="无间道",
        metadata={"year": 2002, "rating": 9.3, "director": "刘伟强"},
    ),
]

db = PineconeVectorStore(
    index_name="llmops",
    embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
    namespace="dataset",
    text_key="text"
)
retriever = db.as_retriever()
# db.add_documents(documents)
print("文档写入完成！")

# 2.创建自查询元数据
metadata_filed_info = [
    AttributeInfo(name="year", description="电影的年份", type="integer"),
    AttributeInfo(name="rating", description="电影的评分", type="float"),
    AttributeInfo(name="director", description="电影的导演", type="string"),
]

document_contents = "电影的名字"
# 修复：不存在gpt-5.4-mini，替换为gpt-4o-mini
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 构造查询构造器
query_constructor = load_query_constructor_runnable(
    llm=llm,
    document_contents=document_contents,
    attribute_info=metadata_filed_info,
    enable_limit=True
)

# 手动传入PineconeTranslator
self_query_retriever = SelfQueryRetriever(
    query_constructor=query_constructor,
    vectorstore=db,
    structured_query_translator=PineconeTranslator(),
    verbose=True
)

# 3.检索示例
print("===== SelfQueryRetriever 检索（带元数据过滤） =====")
docs = self_query_retriever.invoke("查找评分高于9.5分的电影")
for doc in docs:
    print(f"{doc.page_content} | {doc.metadata}")
print(f"命中数量: {len(docs)}")

print("\n===== 普通向量检索（只做向量相似度，不会识别评分过滤） =====")
base_docs = retriever.invoke("查找评分高于9.5分的电影")
for doc in base_docs:
    print(f"{doc.page_content} | {doc.metadata}")
print(f"命中数量: {len(base_docs)}")
