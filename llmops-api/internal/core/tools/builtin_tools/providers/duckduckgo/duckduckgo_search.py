"""
@Time   : 2026/10/13 21:04
@Author : jzy
@File   : duckduckgo_search.py
"""

from langchain_community.tools import DuckDuckGoSearchRun

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class DDGInput(BaseModel):
    """DuckDuckGo搜索工具的输入参数类"""
    query: str = Field(..., description="需要搜索的查询语句")


def duckduckgo_search(**kwargs) -> BaseTool:
    """一个用于DuckDuckGo搜索的工具"""
    return DuckDuckGoSearchRun(
        description="一个注重隐私的搜索工具，当你需要搜索时事时可以使用该工具，工具的输入是一个查询语句",
        args_schema=DDGInput,
    )
