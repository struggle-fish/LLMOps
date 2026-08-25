"""
@Time   : 2026/8/25 17:39
@Author : jzy
@File   : 1.缓冲窗口记忆.py
"""
import dotenv
from operator import itemgetter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_classic.memory import ConversationBufferWindowMemory
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

dotenv.load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是OpenAI开发的聊天机器人，请根据对应的上下问回复用户问题"),
    MessagesPlaceholder("history"),
    ("human", "{query}")
])

memory = ConversationBufferWindowMemory(
    k=2,
    return_messages=True,
    input_key="query"
)

llm = ChatOpenAI(model="gpt-5.4-mini")

chain = RunnablePassthrough.assign(
    history=RunnableLambda(lambda _: memory.load_memory_variables({})) | itemgetter("history")
) | prompt | llm | StrOutputParser()

while True:
    query = input("Human:")

    if query == 'q':
        exit(0)

    chain_input = {
        "query": query
    }
    response = chain.stream(chain_input)
    print("AI:", flush=True, end="")
    output = ""
    for chunk in response:
        output += chunk
        print(chunk, flush=True, end="")
    memory.save_context(chain_input, {"output": output})
    print("")
    print('history:', memory.load_memory_variables({}))
