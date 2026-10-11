"""
@Time   : 2026/10/11 15:54
@Author : jzy
@File   : 1.断点实现人在环路示例.py
"""
from typing import TypedDict, Annotated, Any, Literal
from dotenv import load_dotenv
# 新版：使用原生pydantic v2，移除pydantic_v1
from pydantic import BaseModel, Field
from langchain_community.tools import GoogleSerperRun
from langchain_community.tools.openai_dalle_image_generation import OpenAIDALLEImageGenerationTool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
# ✅ 新版本中断恢复必须导入 Command
from langgraph.types import Command

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


# 图状态定义
class State(TypedDict):
    """图状态数据结构，类型为字典"""
    messages: Annotated[list, add_messages]


tools = [google_serper, dalle]
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_with_tools = llm.bind_tools(tools)


def chatbot(state: State) -> dict:
    """聊天机器人节点，新版节点可以省略config参数（不需要可以删掉）"""
    ai_message = llm_with_tools.invoke(state["messages"])
    return {"messages": [ai_message]}


def route(state: State) -> Literal["tools", "__end__"]:
    """动态路由：判断是否调用工具"""
    ai_message = state["messages"][-1]
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return END


# 构建状态图
graph_builder = StateGraph(State)
graph_builder.add_node("llm", chatbot)
graph_builder.add_node("tools", ToolNode(tools=tools))

# 边配置
graph_builder.add_edge(START, "llm")
graph_builder.add_edge("tools", "llm")
graph_builder.add_conditional_edges("llm", route)

# 编译图：interrupt_before 在进入tools节点前暂停，等待人工确认
checkpointer = MemorySaver()
graph = graph_builder.compile(
    checkpointer=checkpointer,
    interrupt_before=["tools"]
)

# 会话id
config = {"configurable": {"thread_id": 1}}

# 第一次调用图
state = graph.invoke(
    {"messages": [("human", "2024年北京半程马拉松的前3名成绩是多少")]},
    config=config,
)
print("=== 图执行结果 ===")
print(state)

# 获取当前最新状态（推荐新版写法，查看中断信息）
current_state = graph.get_state(config)
last_msg = current_state.values["messages"][-1]

if hasattr(last_msg, "tool_calls") and len(last_msg.tool_calls) > 0:
    print("\n=== 检测到准备调用工具 ===")
    print("工具调用详情: ", last_msg.tool_calls)
    human_input = input("如果需要执行工具请输入yes，否则请输入no: ")
    if human_input.lower() == "yes":
        # ✅【新版重点】使用Command恢复执行，替代旧的 invoke(None, config)
        res = graph.invoke(Command(resume=True), config=config)
        print("\n✅ 工具执行完成，AI回答：")
        print(res["messages"][-1].content)
    else:
        print("\n❌ 用户拒绝调用工具，图程序执行完毕")
else:
    print("\n✅ 无工具调用，直接结束")
