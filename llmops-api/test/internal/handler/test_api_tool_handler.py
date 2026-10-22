"""
@Time   : 2026/10/19 09:18
@Author : jzy
@File   : test_api_tool_handler.py
"""
from contextlib import nullcontext
from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from internal.model import ApiToolProvider, ApiTool
from internal.schema.api_tool_schema import CreateApiToolReq, GetApiToolProviderResq
from internal.service import ApiToolService
from pkg.response import json, HttpCode

openapi_schema_string = """
{
  "server": "https://api.example.com",
  "description": "某天气 API",
  "paths": {
    "/v1/weather": {
      "get": {
        "description": "查询城市天气",
        "operationId": "getWeather",
        "parameters": [
          {
            "name": "city",
            "in": "query",
            "description": "城市名",
            "required": true,
            "type": "str"
          }
        ]
      }
    }
  }
}
"""


class TestApiToolHandler:
    """自定义API插件处理器测试类"""

    @pytest.mark.parametrize("openapi_schema", [
        "123",
        openapi_schema_string
    ])
    def test_validate_openapi_schema(self, openapi_schema, client):
        resp = client.post("/api-tools/validate-openapi-schema", json={
            "openapi_schema": openapi_schema
        })
        assert resp.status_code == 200
        if openapi_schema == '123':
            assert resp.json.get("code") == HttpCode.VALIDATION_ERROR
        elif openapi_schema == openapi_schema_string:
            assert resp.json.get("code") == HttpCode.SUCCESS

    def test_create_and_serialize_openapi_schema(self, client):
        """创建时保留原始规范，读取时返回同名字段。"""
        db = MagicMock()
        db.session.query.return_value.filter_by.return_value.one_or_none.return_value = None
        db.auto_commit.side_effect = nullcontext
        service = ApiToolService(db=db)
        with client.application.test_request_context(method="POST", json={
            "name": "天气工具",
            "icon": "https://api.example.com/icon.png",
            "openapi_schema": openapi_schema_string,
            "headers": [],
        }):
            req = CreateApiToolReq()
            assert req.validate()
            service.create_api_tool(req)

        provider, tool = [call.args[0] for call in db.session.add.call_args_list]
        assert isinstance(provider, ApiToolProvider)
        assert provider.openapi_schema == openapi_schema_string
        assert isinstance(tool, ApiTool)
        assert tool.name == "getWeather"
        assert tool.url == "https://api.example.com/v1/weather"
        provider.id = uuid4()
        provider.created_at = datetime.now()
        result = GetApiToolProviderResq().dump(provider)
        assert result["openapi_schema"] == openapi_schema_string
        assert set(result) == {"id", "name", "icon", "openapi_schema", "headers", "created_at"}
        assert "openapi_schema" in ApiToolProvider.__table__.columns

    def test_validate_missing_openapi_schema(self, client):
        resp = client.post("/api-tools/validate-openapi-schema", json={})
        assert resp.json["code"] == HttpCode.VALIDATION_ERROR

    def test_validate_empty_paths(self, client):
        resp = client.post("/api-tools/validate-openapi-schema", json={
            "openapi_schema": '{"server":"https://api.example.com","description":"天气","paths":{}}'
        })
        assert resp.json["code"] == HttpCode.VALIDATION_ERROR
        assert resp.json["msg"] == "openapi_schema中的paths不能为空且必须是字典"
