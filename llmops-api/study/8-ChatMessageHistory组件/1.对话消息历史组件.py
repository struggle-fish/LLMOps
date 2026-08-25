"""
@Time   : 2026/8/25 13:40
@Author : jzy
@File   : 1.对话消息历史组件.py
"""

from langchain_core.chat_history import InMemoryChatMessageHistory

chat_history = InMemoryChatMessageHistory()

chat_history.add_user_message('你好，我是小铜钱，你是谁')
chat_history.add_ai_message('你好我是你爹')

print(chat_history)
