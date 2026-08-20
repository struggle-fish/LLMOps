"""
@Time   : 2026/8/19 13:19
@Author : jzy
@File   : 1.回调功能实用.py
"""
import time
from typing import Any
from uuid import UUID

import dotenv
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.outputs import GenerationChunk, ChatGenerationChunk, LLMResult
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import StdOutCallbackHandler, BaseCallbackHandler

dotenv.load_dotenv()


class LLMOpsCallbackHandler(BaseCallbackHandler):
    """自定义回调"""
    start_at: float = 0

    def on_chat_model_start(
            self,
            serialized: dict[str, Any],
            messages: list[list[BaseMessage]],
            *,
            run_id: UUID,
            parent_run_id: UUID | None = None,
            tags: list[str] | None = None,
            metadata: dict[str, Any] | None = None,
            **kwargs: Any,
    ) -> Any:
        print("聊天模型开始执行了")
        print("serialized", serialized)
        print("messages", messages)
        self.start_at = time.time()

    def on_llm_end(
            self,
            response: LLMResult,
            *,
            run_id: UUID,
            parent_run_id: UUID | None = None,
            tags: list[str] | None = None,
            **kwargs: Any,
    ) -> Any:
        end_at: float = time.time()
        print("完整输出", response)
        print("消耗时间：", end_at - self.start_at)


prompt = ChatPromptTemplate.from_template("{query}")

llm = ChatOpenAI()

chain = {
            "query": RunnablePassthrough()
        } | prompt | llm | StrOutputParser()

res = chain.stream(
    "你好，你是？",
    config={
        "callbacks": [StdOutCallbackHandler(), LLMOpsCallbackHandler()]
    }
)

for step in res:
    pass
