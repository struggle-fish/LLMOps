"""
@Time   : 2026/10/11 17:38
@Author : jzy
@File   : 1.子图实现多智能体.py
"""
from typing import TypedDict, Any, Annotated
from dotenv import load_dotenv
from langchain_community.tools import GoogleSerperRun
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from langgraph.types import Send

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


class GoogleSerperArgsSchema(BaseModel):
    query: str = Field(description="执行谷歌搜索的查询语句")


google_serper = GoogleSerperRun(
    api_wrapper=GoogleSerperAPIWrapper(),
    args_schema=GoogleSerperArgsSchema,
)


# 状态reducer：字段更新策略
def reduce_str(left: str | None, right: str | None) -> str | None:
    if right is not None and right.strip() != "":
        return right
    return left


# ========== 主图状态 ==========
class AgentState(TypedDict):
    query: Annotated[str, reduce_str]  # 用户原始产品问题
    live_content: Annotated[str, reduce_str]  # 直播文案结果
    xhs_content: Annotated[str, reduce_str]  # 小红书文案结果


# ========== 直播子图状态（带消息+工具调用） ==========
class LiveAgentState(MessagesState):
    query: Annotated[str, reduce_str]
    live_content: Annotated[str, reduce_str]


# ========== 小红书子图状态 ==========
class XHSAgentState(TypedDict):
    query: Annotated[str, reduce_str]
    xhs_content: Annotated[str, reduce_str]


# ---------------- 直播智能体子图 ----------------
def chatbot_live(state: LiveAgentState, config: RunnableConfig) -> Any:
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "你是一个拥有10年经验的直播文案专家，请根据用户提供的产品整理一篇直播带货脚本文案，如果在你的知识库内找不到关于该产品的信息，可以使用搜索工具。"),
        ("human", "{query}"),
        ("placeholder", "{chat_history}"),
    ])
    chain = prompt | llm.bind_tools([google_serper])
    ai_message = chain.invoke({
        "query": state["query"],
        "chat_history": state["messages"]
    })
    return {
        "messages": [ai_message],
        "live_content": ai_message.content,
    }


live_agent_graph = StateGraph(LiveAgentState)
live_agent_graph.add_node("chatbot_live", chatbot_live)
live_agent_graph.add_node("tools", ToolNode([google_serper]))

live_agent_graph.set_entry_point("chatbot_live")
live_agent_graph.add_conditional_edges("chatbot_live", tools_condition)
live_agent_graph.add_edge("tools", "chatbot_live")
# 编译子图
compiled_live_agent = live_agent_graph.compile()


# ---------------- 小红书智能体子图 ----------------
def chatbot_xhs(state: XHSAgentState, config: RunnableConfig) -> Any:
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "你是一个小红书文案大师，请根据用户传递的商品名，生成一篇关于该商品的小红书笔记文案，注意风格活泼，多使用emoji表情。"),
        ("human", "{query}"),
    ])
    chain = prompt | llm | StrOutputParser()
    content = chain.invoke({"query": state["query"]})
    return {"xhs_content": content}


xhs_agent_graph = StateGraph(XHSAgentState)
xhs_agent_graph.add_node("chatbot_xhs", chatbot_xhs)
xhs_agent_graph.add_edge(START, "chatbot_xhs")
xhs_agent_graph.add_edge("chatbot_xhs", END)
compiled_xhs_agent = xhs_agent_graph.compile()


# ---------------- 主图：并行分发任务 Send 【新版核心】 ----------------
def dispatch_agents(state: AgentState) -> list[Send]:
    """分发节点：同时启动两个子图并行执行"""
    return [
        Send("live_agent", {"query": state["query"]}),
        Send("xhs_agent", {"query": state["query"]})
    ]


agent_graph = StateGraph(AgentState)
# 将编译好的子图注册为主图节点
agent_graph.add_node("live_agent", compiled_live_agent)
agent_graph.add_node("xhs_agent", compiled_xhs_agent)

# 入口 -> 分发节点，并行调用两个子图
agent_graph.add_conditional_edges(START, dispatch_agents)
# 两个子图执行完毕自动合并状态到主图，全部完成走向END
agent_graph.add_edge("live_agent", END)
agent_graph.add_edge("xhs_agent", END)

# 编译主图，可选加上MemorySaver做会话记忆
# from langgraph.checkpoint.memory import MemorySaver
# checkpointer = MemorySaver()
# agent = agent_graph.compile(checkpointer=checkpointer)
agent = agent_graph.compile()

# 执行
result = agent.invoke({"query": "潮汕牛肉丸"})
print("===== 直播带货文案 =====")
print(result["live_content"])
print("\n===== 小红书笔记文案 =====")
print(result["xhs_content"])
