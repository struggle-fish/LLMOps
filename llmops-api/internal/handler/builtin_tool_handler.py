"""
@Time   : 2026/10/14 16:20
@Author : jzy
@File   : builtin_tool_handler.py
"""

from dataclasses import dataclass
from injector import inject

from internal.service import BuiltinToolService
from pkg.response import success_json


@inject
@dataclass
class BuiltinToolHandler:
    """"
    内置工具处理器
    """
    builtin_tool_service: BuiltinToolService

    def get_builtin_tools(self):
        """获取所有内置工具信息+提供商信息"""
        builtin_tools = self.builtin_tool_service.get_builtin_tools()
        return success_json(builtin_tools)

    def get_provider_tool(self, provider_name: str, tool_name: str):
        """根据传递的提供商名字+工具名字获取指定工具的信息"""
        pass
