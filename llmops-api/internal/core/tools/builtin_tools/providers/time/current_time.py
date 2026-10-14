"""
@Time   : 2026/10/13 20:58
@Author : jzy
@File   : current_time.py
"""
from datetime import datetime
from langchain_core.tools import BaseTool


class CurrentTimeTool(BaseTool):
    """一个用于获取当前时间的工具"""

    name: str = "current_time"
    description: str = "获取当前时间的工具"

    def _run(self, **kwargs) -> str:
        """获取当前系统的时间并进行格式化后返回"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")


def current_time(**kwargs) -> BaseTool:
    """返回获取当前时间的LangChain工具"""
    return CurrentTimeTool()
