"""
@Time   : 2026/10/8 15:30
@Author : jzy
@File   : 1.XMLAgent示例.py
"""
import dotenv
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_community.tools import GoogleSerperRun
from langchain_community.tools.openai_dalle_image_generation import OpenAIDALLEImageGenerationTool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
import re

dotenv.load_dotenv()


class GoogleSerperArgsSchema(BaseModel):
    query: str = Field(description="执行谷歌搜索的查询语句")


class DallEArgsSchema(BaseModel):
    query: str = Field(description="输入应该是生成图像的文本提示(prompt)")


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
    api_wrapper=DallEAPIWrapper(model="gpt-image-2"),
    args_schema=DallEArgsSchema,
)
tools = {t.name: t for t in [google_serper, dalle]}

# XML提示词
prompt = ChatPromptTemplate.from_messages([
    ("human", """You are a helpful assistant. Help the user answer any questions.
You have access to the following tools:
{tools}
In order to use a tool, you can use <tool></tool> and <tool_input></tool_input> tags. You will then get back a response in the form <observation></observation>
For example, if you have a tool called 'search' that could run a google search, in order to search for the weather in SF you would respond:
<tool>search</tool><tool_input>weather in SF</tool_input>
<observation>64 degrees</observation>
When you are done, respond with a final answer between <final_answer></final_answer>. For example:
<final_answer>The weather in SF is 64 degrees</final_answer>
Begin!
Previous Conversation:
{chat_history}
Question: {input}
{agent_scratchpad}"""),
])

llm = ChatOpenAI(model="gpt-4o-mini")


# 状态定义
class AgentState(TypedDict):
    input: str
    chat_history: str
    scratchpad: str
    messages: Annotated[list[BaseMessage], operator.add]


# 模型调用节点
def call_model(state: AgentState):
    p = prompt.format(
        tools="\n".join([f"{t.name}:{t.description}" for t in tools.values()]),
        chat_history=state["chat_history"],
        input=state["input"],
        agent_scratchpad=state["scratchpad"]
    )
    resp = llm.invoke([HumanMessage(content=p)])
    return {"messages": [resp]}


# 解析XML，判断是否调用工具
def route(state: AgentState):
    last_msg = state["messages"][-1].content
    if "<final_answer>" in last_msg:
        return "end"
    elif "<tool>" in last_msg and "<tool_input>" in last_msg:
        return "tool"
    else:
        return "end"


# 工具执行节点
def run_tool(state: AgentState):
    last_msg = state["messages"][-1].content
    tool_name = re.search(r"<tool>(.*?)</tool>", last_msg).group(1).strip()
    tool_input = re.search(r"<tool_input>(.*?)</tool_input>", last_msg).group(1).strip()
    tool = tools[tool_name]
    obs = tool.invoke(tool_input)
    new_scratch = state["scratchpad"] + f"\n{last_msg}\n<observation>{obs}</observation>"
    return {"scratchpad": new_scratch}


# 构建图
builder = StateGraph(AgentState)
builder.add_node("agent", call_model)
builder.add_node("tool", run_tool)
builder.set_entry_point("agent")
builder.add_conditional_edges("agent", route, {"tool": "tool", "end": END})
builder.add_edge("tool", "agent")
graph = builder.compile()

# 运行
res = graph.invoke({
    "input": "马拉松的世界记录是多少？",
    "chat_history": "",
    "scratchpad": "",
    "messages": []
})
print(res["messages"][-1].content)
