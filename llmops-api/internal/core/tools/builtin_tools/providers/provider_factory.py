"""
@Time   : 2026/10/12 22:24
@Author : jzy
@File   : provider_factory.py
"""
import os.path
from typing import Any

import yaml
from injector import inject, singleton

from internal.core.tools.builtin_tools.entities import ProviderEntity, Provider


@inject
@singleton
class ProviderFactory:
    """服务提供商工厂类"""
    provider_map: dict[str, Provider] = {}

    def __init__(self):
        """构造函数，初始化对应的provider_tool_map"""
        self._get_provider_tool_map()

    def get_provider(self, provider_name: str) -> Provider:
        """获取服务提供商"""
        return self.provider_map.get(provider_name)

    def get_providers(self) -> list[Provider]:
        """获取所有服务提供商"""
        return list(self.provider_map.values())

    def get_provider_entities(self) -> list[ProviderEntity]:
        """获取所有服务提供商的实体"""
        return [provider.provider_entity for provider in self.provider_map.values()]

    def get_tool(self, provider_name: str, tool_name: str) -> Any:
        """根据服务商的名字+工具名字，获取特定的工具函数"""
        provider = self.get_provider(provider_name)
        if provider:
            return provider.get_tool(tool_name)
        return None

    def _get_provider_tool_map(self):
        """项目初始化的时候获取服务提供商，工具的映射关系并填充provider_tool_map"""
        # 1.检测provider_map是否为空
        if self.provider_map:
            return
        # 2.获取当前文件/类所在的文件夹路径
        current_path = os.path.abspath(__file__)
        providers_path = os.path.dirname(current_path)
        providers_yaml_path = os.path.join(providers_path, "providers.yaml")

        # 3.读取providers.yaml的数据
        with open(providers_yaml_path, "r", encoding="utf-8") as f:
            providers_yaml_data = yaml.load(f, Loader=yaml.FullLoader)

        # 4.遍历providers.yaml的数据，填充provider_tool_map
        for idx, provider_data in enumerate(providers_yaml_data):
            provider_entity = ProviderEntity(**provider_data)  # 校验数据是否符合ProviderEntity的要求
            self.provider_map[provider_entity.name] = Provider(
                name=provider_entity.name,
                position=idx + 1,
                provider_entity=provider_entity
            )  # 填充provider_map
