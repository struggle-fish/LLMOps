"""
@Time   : 2026/10/12 23:03
@Author : jzy
@File   : provider_entity.py
"""
import os.path
from typing import Any

import yaml
from pydantic import BaseModel, Field

from internal.core.tools.builtin_tools.entities import ToolEntity
from internal.lib.helper import dynamic_import


class ProviderEntity(BaseModel):
    """"服务提供商实体，映射的数据是provider.yaml中的数据"""
    name: str  # 名字
    label: str  # 标签，给前端看的
    description: str  # 描述
    icon: str  # 图标地址
    background: str  # 图标的颜色
    category: str  # 分类信息


class Provider(BaseModel):
    """服务提供商，在该类下，可以获取到该服务提供商的所有工具，描述，图标等多个信息"""
    name: str  # 服务提供商的名字
    position: int  # 服务提供商的排序序号，与工厂生成的整数索引保持一致
    provider_entity: ProviderEntity  # 服务提供商的实体
    tool_func_map: dict[str, Any] = Field(default_factory=dict)  # 服务提供商的工具函数映射关系
    tool_entity_map: dict[str, ToolEntity] = Field(default_factory=dict)  # 服务提供商的工具实体映射关系

    def __init__(self, **kwargs):
        """构造函数，完成对应服务提供商的初始化"""
        super().__init__(**kwargs)
        self._provider_init()

    class Config:
        """配置类"""
        protected_namespaces = ()

    def get_tool(self, tool_name: str):
        """获取服务提供商的工具函数"""
        return self.tool_func_map.get(tool_name)

    def get_tool_entity(self, tool_name: str) -> ToolEntity:
        """获取服务提供商的工具实体"""
        return self.tool_entity_map.get(tool_name)

    def get_tool_entities(self) -> list[ToolEntity]:
        """获取服务提供商的所有工具实体"""
        return list(self.tool_entity_map.values())

    def _provider_init(self) -> None:
        """服务提供商初始化函数"""
        # 1. 获取当前类的路径，计算出该服务提供商的工具文件夹路径
        current_path = os.path.abspath(__file__)
        entities_path = os.path.dirname(current_path)
        provider_path = os.path.join(os.path.dirname(entities_path), "providers", self.name)

        # 2.读取 positions.yaml，按配置顺序加载服务提供商的工具
        position_yaml_path = os.path.join(provider_path, "positions.yaml")
        with open(position_yaml_path, encoding="utf-8") as f:
            position_yaml_data = yaml.safe_load(f)

        # 3.循环读取位置信息获取服务提供商的工具名字
        for tool_name in position_yaml_data:
            # 4.组装获取tool.yaml的数据
            tool_yaml_path = os.path.join(provider_path, f"{tool_name}.yaml")
            with open(tool_yaml_path, encoding="utf-8") as f:
                tool_yaml_data = yaml.safe_load(f)

            # 5.将工具的实体类和函数映射关系填充到tool_entity_map和tool_func_map中
            self.tool_entity_map[tool_name] = ToolEntity(**tool_yaml_data)

            # 6.动态导入对应的工具函数，并填充到tool_func_map中
            tool_module_path = f"internal.core.tools.builtin_tools.providers.{self.name}"
            tool_function = dynamic_import(tool_module_path, tool_name)
            self.tool_func_map[tool_name] = tool_function
