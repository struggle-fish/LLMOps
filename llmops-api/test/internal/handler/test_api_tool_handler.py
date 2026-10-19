"""
@Time   : 2026/10/19 09:18
@Author : jzy
@File   : test_api_tool_handler.py
"""
import pytest

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
