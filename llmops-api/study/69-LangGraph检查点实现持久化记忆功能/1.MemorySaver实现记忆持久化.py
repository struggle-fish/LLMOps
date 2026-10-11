"""
@Time   : 2026/10/11 13:49
@Author : jzy
@File   : 1.MemorySaver实现记忆持久化.py
"""
from dotenv import load_dotenv
from langchain_community.tools import GoogleSerperRun
from langchain_community.tools.openai_dalle_image_generation import OpenAIDALLEImageGenerationTool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
# 新版推荐显式导入消息类型
from langchain_core.messages import HumanMessage

load_dotenv()


class GoogleSerperArgsSchema(BaseModel):
    query: str = Field(description="执行谷歌搜索的查询语句")


class DallEArgsSchema(BaseModel):
    query: str = Field(description="输入应该是生成图像的文本提示(prompt)")


# 1.定义工具与工具列表
google_serper = GoogleSerperRun(
    name="google_serper",
    description=(
        "一个低成本的谷歌搜索API。"
        "当你需要回答有关时事的问题时，可以调用该工具。"
        "该工具的输入是搜索查询语句。"
    ),
    args_schema=GoogleSerperArgsSchema,
    api_wrapper=GoogleSerperAPIWrapper(),
)

dalle = OpenAIDALLEImageGenerationTool(
    name="openai_dalle",
    api_wrapper=DallEAPIWrapper(model="dall-e-3"),
    args_schema=DallEArgsSchema,
)

tools = [google_serper, dalle]

# 2.创建大语言模型
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 3.使用预构建的函数创建ReACT智能体 + 记忆检查点
checkpointer = MemorySaver()
# 会话唯一ID，同一个对话必须保持不变
config = {"configurable": {"thread_id": "1"}}
agent = create_react_agent(model=model, tools=tools, checkpointer=checkpointer)

# 4.调用智能体并输出内容
res1 = agent.invoke(
    {"messages": [HumanMessage(content="你好，我叫慕小课，我喜欢游泳打球，你喜欢什么呢?")]},
    config=config,
)
print("第一轮输出：")
print(res1["messages"][-1].content)

# ✅【重点修复】新版LangGraph每次invoke**都必须传入同一个config**，否则不读取记忆！
res2 = agent.invoke(
    {"messages": [HumanMessage(content="你知道我叫什么吗?")]},
    config=config,
)
print("\n第二轮输出：")
print(res2["messages"][-1].content)
