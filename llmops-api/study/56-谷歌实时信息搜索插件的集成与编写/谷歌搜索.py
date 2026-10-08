"""
@Time   : 2026/10/7 18:40
@Author : jzy
@File   : 谷歌搜索.py
"""

import os
import dotenv
from typing import Any, Type
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from langchain_community.utilities import SerpAPIWrapper

# 加载环境变量
dotenv.load_dotenv()


# 参数模型
class SerpApiArgsSchema(BaseModel):
    query: str = Field(description="谷歌搜索查询词")


# 自定义搜索工具，继承BaseTool，和高德天气工具写法完全对齐
class SerpApiSearchTool(BaseTool):
    name: str = "serpapi_search"
    description: str = (
        "谷歌实时搜索工具，用于查询时事、最新数据、实时信息。"
        "当需要时效性内容时调用，输入为搜索query。"
    )
    args_schema: Type[BaseModel] = SerpApiArgsSchema

    def _run(self, **kwargs: Any) -> str:
        query = kwargs.get("query")
        serpapi_key = os.getenv("SERPAPI_API_KEY")
        wrapper = SerpAPIWrapper(serpapi_api_key=serpapi_key)
        result = wrapper.run(query)
        return str(result)


# 实例化工具
serp_search = SerpApiSearchTool()

if __name__ == "__main__":
    res = serp_search.invoke({"query": "马拉松的世界记录是多少"})
    print(res)
