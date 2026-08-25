"""
@Time   : 2026/8/25 14:13
@Author : jzy
@File   : 2.文件对话消息历史组件.py
"""
import os
from typing import Any

import dotenv

from openai import OpenAI
from langchain_community.chat_message_histories import FileChatMessageHistory

dotenv.load_dotenv()

# 创建客户端记忆
client = OpenAI(
    base_url=os.getenv('OPENAI_BASE_URL'),
    api_key=os.getenv('OPENAI_API_KEY')
)
chat_history = FileChatMessageHistory('./memory.txt')

while True:
    query = input('Human:')

    if query == 'q':
        exit(0)

    system_prompt = (
        "你是OpenAi开发的聊天机器人，可以根据相应的上下文回复用户信息，上下文存放的是人类与你对话的信息列表\n\n"
        f"<context>{chat_history}</context>\n\n"
    )
    response = client.chat.completions.create(
        model=os.getenv('OPENAI_MODEL'),
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": query
            }
        ],
        stream=True
    )
    print("AI:", flush=True, end="")
    ai_content = ""
    for chunk in response:
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta
        if delta.content is None:
            continue
        ai_content += delta.content
        print(delta.content, flush=True, end="")
    chat_history.add_user_message(query)
    chat_history.add_ai_message(ai_content)
    print("")
