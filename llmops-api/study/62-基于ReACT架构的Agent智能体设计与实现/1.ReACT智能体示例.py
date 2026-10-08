"""
@Time   : 2026/10/8 13:27
@Author : jzy
@File   : 1.ReACT智能体示例.py
"""
import dotenv
# 改动点：导入从langgraph.prebuilt


from langchain.agents import create_agent
from langchain_community.tools import GoogleSerperRun
from langchain_community.utilities import GoogleSerperAPIWrapper
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()


class GoogleSerperArgsSchema(BaseModel):
    query: str = Field(description="执行谷歌搜索的查询语句")


# 1.定义工具与工具列表（工具代码完全不用改动！）
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
tools = [google_serper]

# 2.定义大语言模型，使用Crazyrouter中转模型 gpt-5.4-mini
llm = ChatOpenAI(model="gpt-5.4-mini", temperature=0)

# 3.创建ReAct智能体，LangGraph内部自动处理工具调用循环，不再需要AgentExecutor
agent = create_agent(
    model=llm,
    tools=tools,
    # 可选：系统提示词，用来约束助手行为，不再使用旧版Thought/Action格式模板
    system_prompt="你是一个擅长使用搜索工具的助手，遇到需要实时信息的问题，请调用google_serper工具搜索。"
)

# 4.执行智能体，入参格式变更，不再用{"input": "..."}
res = agent.invoke({"messages": [("user", "马拉松的最新世界记录是多少？")]})

# 打印最终回答
print(res["messages"][-1].content)

# 如果想看完整思考/工具调用过程，打印全部消息
# for msg in res["messages"]:
#     print(f"{msg.type}: {msg.content}")
