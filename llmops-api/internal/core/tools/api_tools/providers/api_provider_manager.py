"""
@Time   : 2026/10/26 22:31
@Author : jzy
@File   : api_provider_manager.py
"""

from dataclasses import dataclass

from injector import inject
from langchain_core.tools import BaseTool

from pydantic import BaseModel


@inject
@dataclass
class ApiProviderManager(BaseModel):
    """API工具提供者管理器，能根据传递的工具配置信息生成自定义LangChain 工具"""

    def get_tool(self, tool_entity) -> BaseTool:
        """根据传递的配置后去自定义API工具"""
