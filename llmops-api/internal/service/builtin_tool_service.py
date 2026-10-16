"""
@Time   : 2026/10/14 16:40
@Author : jzy
@File   : builtin_tool_service.py
"""
import mimetypes
import os
from typing import Any

from flask import current_app
from injector import inject
from dataclasses import dataclass

from pydantic import BaseModel

from internal.core.tools.builtin_tools.providers.builtin_provider_manager import BuiltinProviderManager
from internal.core.tools.builtin_tools.categories.builtin_category_manager import BuiltinCategoryManager

from internal.exception import NotFoundException


@inject
@dataclass
class BuiltinToolService:
    """
    内置工具服务
    """

    builtin_provider_manager: BuiltinProviderManager
    builtin_category_manager: BuiltinCategoryManager

    def get_builtin_tools(self) -> list:
        """获取所有内置工具信息+提供商信息"""
        # 1. 获取所有服务提供商
        providers = self.builtin_provider_manager.get_providers()
        # 2. 遍历服务提供商，获取每个提供商的工具信息
        builtin_tools = []
        for provider in providers:
            provider_entity = provider.provider_entity
            builtin_tool = {
                **provider_entity.model_dump(exclude=["icon"]),
                "tools": []
            }
            # 3. 循环遍历提取提供者的所有工具实体
            for tool_entity in provider.get_tool_entities():
                # 4. 从提供者中获取工具函数
                tool = provider.get_tool(tool_entity.name)
                # 5. 构建工具实体信息
                tool_dict = {
                    **tool_entity.model_dump(),
                    "inputs": self.get_tool_inputs(tool)
                }
                builtin_tool["tools"].append(tool_dict)
            builtin_tools.append(builtin_tool)

        return builtin_tools

    def get_provider_tool(self, provider_name: str, tool_name: str) -> dict:
        """根据传递的提供商名字+工具名字获取指定工具的信息"""

        # 1. 获取内置的供应商
        provider = self.builtin_provider_manager.get_provider(provider_name)
        if provider is None:
            raise NotFoundException(f"该提供商{provider_name}不存在")
        # 2. 获取该提供商下对应的工具
        tool_entity = provider.get_tool_entity(tool_name)
        if tool_entity is None:
            raise NotFoundException(f"该工具{tool_name}不存在")
        # 3. 组装提供商和工具实体信息
        provider_entity = provider.provider_entity
        tool = provider.get_tool(tool_name)
        builtin_tool = {
            "provider": {
                **provider_entity.model_dump(exclude=["icon"]),
            },
            "created_at": provider_entity.created_at,
            **tool_entity.model_dump(),
            "inputs": self.get_tool_inputs(tool)
        }
        return builtin_tool

    def get_provider_icon(self, provider_name: str) -> tuple[bytes, str]:
        """根据传递的提供商获取icon图标信息流"""
        # 1. 获取对应的工具提供者
        provider = self.builtin_provider_manager.get_provider(provider_name)
        if not provider:
            raise NotFoundException(f"该工具提供者{provider_name}不存在")
        # 2. 获取项目的根路径信息
        root_path = os.path.dirname(os.path.dirname(current_app.root_path))

        # 3. 拼接提供者所在文件夹
        provider_path = os.path.join(
            root_path,
            "internal",
            "core",
            "tools",
            "builtin_tools",
            "providers",
            provider_name
        )
        # 4. 拼接icon对应的路径
        icon_path = os.path.join(provider_path, "_asset", provider.provider_entity.icon)

        # 5.检测icon是否存在
        if not os.path.exists(icon_path):
            raise NotFoundException(f"该工具提供者_asset下未提供图标")

        # 6.读取icon的类型
        mimetype, _ = mimetypes.guess_type(icon_path)
        mimetype = mimetype or "application/octet-stream"

        # 7.读取icon字节数据
        with open(icon_path, "rb") as f:
            byte_data = f.read()
            return byte_data, mimetype

    def get_categories(self) -> list[str, Any]:
        """获取所有的内置分类信息，涵盖了category, name , icon"""
        category_map = self.builtin_category_manager.get_category_map()
        return [{
            "name": category["entity"].name,
            "category": category["entity"].category,
            "icon": category["icon"]
        } for category in category_map.values()]

    @classmethod
    def get_tool_inputs(cls, tool) -> list:
        """
        检测下工具是否有args_schema属性，并且是BaseModel的子类，如果有则提取其参数信息
        """
        inputs = []
        if hasattr(tool, "args_schema") and issubclass(tool.args_schema, BaseModel):
            # Pydantic v2 的字段直接提供描述、类型注解和必填判断，避免访问已移除的 v1 属性。
            for field_name, model_field in tool.args_schema.model_fields.items():
                input_info = {
                    "name": field_name,
                    "description": model_field.description or "",
                    "type": model_field.annotation.__name__,
                    "required": model_field.is_required(),
                }
                inputs.append(input_info)
        return inputs
