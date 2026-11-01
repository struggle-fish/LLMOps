"""
@Time   : 2026/10/26 22:31
@Author : jzy
@File   : api_provider_manager.py
"""

from dataclasses import dataclass
from typing import Callable, Optional, Type

import requests
from injector import inject
from langchain_core.tools import BaseTool, StructuredTool

from pydantic import BaseModel, create_model, Field
from internal.core.tools.api_tools.entities import ParameterIn, ToolEntity, ParameterTypeMap



"""
把数据库中配置的 API 信息，动态转换成 LangChain Agent 可以识别、理解并调用的工具。

你不需要为每一个 API 单独写 Python 函数，只需要配置接口的名称、地址、请求方式和参数，就能自动生成对应的工具。


"""

@inject
@dataclass
class ApiProviderManager(BaseModel):
    """API工具提供者管理器，能根据传递的工具配置信息生成自定义LangChain 工具"""


    @classmethod
    def _create_tool_func_from_tool_entity(cls, tool_entity: ToolEntity) -> Callable:
        """创建真正发送 HTTP 请求的函数"""
        """根据传递的信息创建发起 API 的请求的函数"""
        def tool_func(**kwargs) -> str:
            """API 工具请求函数"""
            # 1. 定义变量存储来自 path / query / header / cookie / request_body中的数据
            parameters = {
                ParameterIn.PATH: {},
                ParameterIn.HEADER: {},
                ParameterIn.QUERY: {},
                ParameterIn.COOKIE: {},
                ParameterIn.REQUEST_BODY: {}
            }
            # 2. 更改参数结构映射
            parameter_map = {
                parameter.get("name"): parameter for parameter in tool_entity.parameters
            }
            """
            parameter.get("name"): parameter 
            即 key: value的格式
            tool_entity.parameters = [
                {"name": "username", "type": "string", "required": True},
                {"name": "age", "type": "integer", "required": False},
                {"name": "email", "type": "string", "required": True}
            ]
            
            parameter_map: {
                "username": {
                    "name": "username",
                    "type": "string",
                    "required": True
                },
                "age": {
                    "name": "age",
                    "type": "integer",
                    "required": False
                },
                "email": {
                    "name": "email",
                    "type": "string",
                    "required": True
                }
            }
            
            """
            header_map= {
                header.get("name"): header.get("value") for header in tool_entity.headers
            }

            # 3. 循环遍历传递的所有字段并校验
            for key, value in kwargs.items():
                # 4.提取键值对关联的字段并校验
                parameter = parameter_map.get(key)
                if parameter is None:
                    continue
                # 5. 将参数存储到合适的位置上,默认在 query 上
                parameters[parameter.get("in", ParameterIn.QUERY)][key] = value

            # 6. 构建 request 请求并返回采集的内容
            return requests.request(
                method=tool_entity.method,
                url=tool_entity.url.format(**parameters[ParameterIn.PATH]),
                params=parameters[ParameterIn.QUERY],
                json=parameters[ParameterIn.REQUEST_BODY],
                headers={**header_map, **parameters[ParameterIn.HEADER]},
                cookies=parameters[ParameterIn.COOKIE],
            ).text

        return tool_func


    @classmethod
    def _create_model_from_parameters(cls, parameters: list[dict]) -> Type[BaseModel]:
        """根据 API 参数配置动态生成 Pydantic 参数模型"""
        """根据传递的 parameters参数创建 BaseModel 子类"""
        fields = {}
        for parameter in parameters:
            field_name = parameter.get("name")
            field_type = ParameterTypeMap.get(parameter.get("type"), str)
            field_required = parameter.get("required", True)
            field_description = parameter.get("description", "")
            fields[field_name] = (
                field_type if field_required else Optional[field_type],
                Field(description=field_description),
            )

        return create_model("DynamicModel", **fields)



    def get_tool(self, tool_entity: ToolEntity) -> BaseTool:
        """根据传递的配置后去自定义API工具"""
        """将请求函数和参数模型组合成 LangChain 工具"""
        return StructuredTool(
            func=self._create_tool_func_from_tool_entity(tool_entity),
            name=f"{tool_entity.id}_{tool_entity.name}",
            description=tool_entity.description,
            args_schema=self._create_model_from_parameters(tool_entity.parameters),
        )
