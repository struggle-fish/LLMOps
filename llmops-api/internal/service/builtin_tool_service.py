"""
@Time   : 2026/10/14 16:40
@Author : jzy
@File   : builtin_tool_service.py
"""

from injector import inject
from dataclasses import dataclass

from pydantic import BaseModel

from internal.core.tools.builtin_tools.providers.builtin_provider_manager import BuiltinProviderManager


@inject
@dataclass
class BuiltinToolService:
    """
    内置工具服务
    """

    builtin_provider_manager: BuiltinProviderManager

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
                # 4. 构建工具实体信息
                tool_dict = {
                    **tool_entity.model_dump(),
                    "inputs": []
                }
                # 5. 从提供者中获取工具函数
                tool = provider.get_tool(tool_entity.name)
                # 6. 检测下工具是否有args_schema属性，并且是BaseModel的子类，如果有则提取其参数信息
                if hasattr(tool, "args_schema") and issubclass(tool.args_schema, BaseModel):
                    inputs = []
                    for field_name, model_field in tool.args_schema.model_fields.items():
                        input_info = {
                            "name": field_name,
                            "description": model_field.field_info.description or "",
                            "type": str(model_field.outer_type_.__name__),
                            "required": model_field.required,
                        }
                        inputs.append(input_info)
                    tool_dict["inputs"] = inputs
                builtin_tool["tools"].append(tool_dict)
            builtin_tools.append(builtin_tool)

        return builtin_tools

        # 3. 除了工具实体，还需要提取工具的inputs代表大语言模型的输入参数信息
        # 4. 组装提取所有信息为list 并返回

    def get_provider_tool(self, provider_name: str, tool_name: str) -> dict:
        """根据传递的提供商名字+工具名字获取指定工具的信息"""
        pass
