"""
@Time   : 2026/10/18 15:19
@Author : jzy
@File   : api_tool_handler.py
"""
from dataclasses import dataclass
from uuid import UUID

from flask import request
from injector import inject

from internal.schema.api_tool_schema import (
    ValidateOpenAPISchemaReq,
    CreateApiToolReq,
    GetApiToolProviderResq,
    GetApiToolResp,
    GetApiToolProvidersWithPageReq,
    GetApiToolProvidersWithPageResp,
    UpdateApiToolProviderReq
)
from pkg.paginator import PageModel
from pkg.response import validate_error_json, success_json, success_message
from internal.service import ApiToolService


@inject
@dataclass
class ApiToolHandler:
    """自定义API插件处理器"""
    api_tool_service: ApiToolService

    def get_api_tool_provider_with_page(self):
        """获取api工具提供者列表信息，该接口支持分页"""
        req = GetApiToolProvidersWithPageReq(formdata=request.args)
        if not req.validate():
            return validate_error_json(req.errors)

        api_tool_providers, paginator = self.api_tool_service.get_api_tool_providers_with_page(req)

        resp = GetApiToolProvidersWithPageResp(many=True)

        return success_json(PageModel(list=resp.dump(api_tool_providers), paginator=paginator))

    def create_api_tool_provider(self):
        """创建自定义api工具"""
        # 1. 提取请求的数据并进行校验
        req = CreateApiToolReq()
        if not req.validate():
            return validate_error_json(req.errors)
        # 2. 调用服务创建API工具
        self.api_tool_service.create_api_tool(req)
        return success_message("创建自定义api插件成功")

    def update_api_tool_provider(self, provider_id: UUID):
        """"更新自定义 API 工具提供者信息"""
        req = UpdateApiToolProviderReq()
        if not req.validate():
            return validate_error_json(req.errors)

        self.api_tool_service.update_api_tool_provider(provider_id, req)

        return success_message("更新自定义 API 插件成功")

    def get_api_tool(self, provider_id: UUID, tool_name: str):
        """根据传递的provider_id + tool_name 获取工具的详情"""
        api_tool = self.api_tool_service.get_api_tool(provider_id, tool_name)
        resp = GetApiToolResp()
        return success_json(resp.dump(api_tool))

    def get_api_tool_provider(self, provider_id: UUID):
        """根据传递的provider_id获取工具提供者的原始信息"""
        api_tool_provider = self.api_tool_service.get_api_tool_provider(provider_id)

        resp = GetApiToolProviderResq()
        return success_json(resp.dump(api_tool_provider))

    def delete_api_tool(self, provider_id: UUID):
        """根据传递的provider_id删除对应的工具提供者信息"""
        self.api_tool_service.delete_api_tool_provider(provider_id)

        return success_message("删除自定义api插件成功")

    def validate_openapi_schema(self):
        """校验传递的openapi_schema字符串是否正确"""
        # 1. 提取前端数据进行校验
        req = ValidateOpenAPISchemaReq()
        if not req.validate():
            return validate_error_json(req.errors)
        # 2.调用服务并解析传递的数据
        self.api_tool_service.parse_openapi_schema(req.openapi_schema.data)

        return success_json("校验成功")
