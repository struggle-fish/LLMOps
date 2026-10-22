"""
@Time   : 2026/10/18 15:27
@Author : jzy
@File   : api_tool_service.py
"""
from typing import Any
from uuid import UUID

from injector import inject
from dataclasses import dataclass

import json

from internal.core.tools.api_tools.entities import OpenAPISchema
from internal.exception import ValidationErrorException, NotFoundException
from internal.model import ApiToolProvider, ApiTool
from internal.schema.api_tool_schema import CreateApiToolReq
from pkg.sqlalchemy import SQLAlchemy


@inject
@dataclass
class ApiToolService:
    """自定义API插件服务"""
    db: SQLAlchemy

    def get_api_tool_provider(self, provider_id: UUID) -> ApiToolProvider:
        """根据传递的provider_id获取API工具提供者信息"""
        # todo:等待授权认证模块完成进行切换调整
        account_id = "46db30d1-3199-4e79-a0cd-abf12fa6858f"
        # 1. 查询数据库获取对应的数据
        api_tool_provider = self.db.session.query(ApiToolProvider).get(provider_id)
        # 2. 校验数据是否为空，并且判断该数据是否属于当前账号
        if api_tool_provider is None or str(api_tool_provider.account_id) != account_id:
            raise NotFoundException("该工具提供者不存在")
        return api_tool_provider

    def create_api_tool(self, req: CreateApiToolReq) -> None:
        """根据传递的请求创建自定义api工具"""
        # todo:等待授权认证模块完成进行切换调整
        account_id = "46db30d1-3199-4e79-a0cd-abf12fa6858f"

        # 1、校验并提取 openapi_schema对应的数据
        openapi_schema = self.parse_openapi_schema(req.openapi_schema.data)

        # 2、查询当前登录的账号是否已经创建了同名的工具提供者，如果是则抛出错误
        api_tool_provider = self.db.session.query(ApiToolProvider).filter_by(
            account_id=account_id,
            name=req.name.data
        ).one_or_none()
        if api_tool_provider:
            raise ValidationErrorException(f"该工具提供者名字{req.name.data}已存在")

        # 3、开启数据库的自动提交
        with self.db.auto_commit():
            # 4. 首先创建工具提供者，并获取工具提供者的id信息，然后在创建工具信息
            api_tool_provider = ApiToolProvider(
                account_id=account_id,
                name=req.name.data,
                icon=req.icon.data,
                description=openapi_schema.description,
                openapi_schema=req.openapi_schema.data,
                headers=req.headers.data
            )
            self.db.session.add(api_tool_provider)
            self.db.session.flush()

            # 5. 创建api工具并关联api_tool_provider
            for path, path_item in openapi_schema.paths.items():
                for method, method_item in path_item.items():
                    api_tool = ApiTool(
                        account_id=account_id,
                        provider_id=api_tool_provider.id,
                        name=method_item.get("operationId"),
                        description=method_item.get("description"),
                        url=f"{openapi_schema.server}{path}",
                        method=method,
                        parameters=method_item.get("parameters", [])
                    )
                    self.db.session.add(api_tool)

    @classmethod
    def parse_openapi_schema(cls, openapi_schema_str: str) -> OpenAPISchema:
        """解析传递的openapi_schema字符串，如果出错就抛出错误"""
        try:
            data = json.loads(openapi_schema_str.strip())
            if not isinstance(data, dict):
                raise
        except Exception as e:
            raise ValidationErrorException("传递数据必须符合OpenAPI规范的JSON字符串")

        return OpenAPISchema(**data)
