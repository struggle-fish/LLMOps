"""
@Time   : 2026/10/18 15:27
@Author : jzy
@File   : api_tool_service.py
"""
from typing import Any

from injector import inject
from dataclasses import dataclass

import json

from internal.core.tools.api_tools.entities import OpenAPISchema
from internal.exception import ValidationErrorException


@inject
@dataclass
class ApiToolService:
    """自定义API插件服务"""

    @classmethod
    def parse_openai_schema(cls, openai_schema_str: str) -> OpenAPISchema:
        """解析传递的openai_schema字符串，如果出错就抛出错误"""
        try:
            data = json.loads(openai_schema_str.strip())
            if not isinstance(data, dict):
                raise
        except Exception as e:
            raise ValidationErrorException("传递数据必须符合OpenAPI规范的JSON字符串")

        return OpenAPISchema(**data)
