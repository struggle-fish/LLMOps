"""
@Time   : 2026/8/26 14:07
@Author : jzy
@File   : 1.使用示例.py
"""
import dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import FileChatMessageHistory

dotenv.load_dotenv()

store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = FileChatMessageHistory(f"./chat_history_{session_id}.txt")
    return store[session_id]


prompt = ChatPromptTemplate.from_messages([
    ("system", "你是OpenAI开发的聊天机器人，请根据对应的上下问回复用户问题"),
    MessagesPlaceholder("history"),
    ("human", "{query}")
])

llm = ChatOpenAI(model="gpt-5.4-mini")

chain = prompt | llm | StrOutputParser()

# 包装链
with_message_chain = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="query",
    history_messages_key="history",
)

while True:
    query = input("Human:")

    if query == 'q':
        exit(0)

    response = with_message_chain.stream(
        {"query": query},
        config={
            "configurable": {
                "session_id": '小铜钱'
            }
        }
    )
    print("AI:", flush=True, end="")
    output = ""
    for chunk in response:
        output += chunk
        print(chunk, flush=True, end="")
    print("")
