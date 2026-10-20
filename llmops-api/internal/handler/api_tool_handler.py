"""
@Time   : 2026/10/18 15:19
@Author : jzy
@File   : api_tool_handler.py
"""
from dataclasses import dataclass
from injector import inject

from internal.schema.api_tool_schema import ValidateOpenAPISchemaReq, CreateApiToolReq
from pkg.response import validate_error_json, success_json, success_message
from internal.service import ApiToolService


@inject
@dataclass
class ApiToolHandler:
    """自定义API插件处理器"""
    api_tool_service: ApiToolService

    def create_api_tool(self):
        """创建自定义api工具"""
        # 1. 提取请求的数据并进行校验
        req = CreateApiToolReq()
        if not req.validate():
            return validate_error_json(req.errors)
        # 2. 调用服务创建API工具
        self.api_tool_service.create_api_tool(req)
        return success_message("创建自定义api插件成功")

    def validate_openai_schema(self):
        """校验传递的open_schema字符串是否正确"""
        # 1. 提取前端数据进行校验
        req = ValidateOpenAPISchemaReq()
        if not req.validate():
            return validate_error_json(req.errors)
        # 2.调用服务并解析传递的数据
        self.api_tool_service.parse_openai_schema(req.openapi_schema.data)

        return success_json("校验成功")
