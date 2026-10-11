"""
@Time   : 2026/10/9 07:04
@Author : jzy
@File   : 1.基础LangGraph示例.py
"""
from typing import TypedDict, Annotated, Any
import dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.config import get_config
from langgraph.types import RunnableConfig  # 导入RunnableConfig

dotenv.load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")


# 1.创建状态图，并使用GraphState作为状态数据
class State(TypedDict):
    """图结构的状态数据"""
    messages: Annotated[list, add_messages]
    use_name: str


def chatbot(state: State) -> Any:
    """聊天机器人节点，使用大语言模型根据传递的消息列表生成内容"""
    # 如果需要读取config，在这里获取，不要再放到函数参数
    config: RunnableConfig = get_config()
    print("当前config：", config)

    ai_message = llm.invoke(state["messages"])
    return {"messages": [ai_message], "use_name": "chatbot"}


graph_builder = StateGraph(State)
# 2.添加节点
graph_builder.add_node("llm", chatbot)
# 3.添加边
graph_builder.add_edge(START, "llm")
graph_builder.add_edge("llm", END)

# 4.编译图为Runnable可运行组件
graph = graph_builder.compile()
# 5.调用图架构应用
print(graph.invoke({"messages": [("human", "你好，你是谁，我叫慕小课，我喜欢打篮球游泳")], "use_name": "graph"}))
