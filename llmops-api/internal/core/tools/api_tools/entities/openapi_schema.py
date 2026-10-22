"""
@Time   : 2026/10/18 15:36
@Author : jzy
@File   : openapi_schema.py
"""
from pydantic import AliasChoices, BaseModel, Field, field_validator

from internal.exception import ValidationErrorException

from enum import Enum


class ParameterType(str, Enum):
    """参数支持的类型"""
    STR: str = "str"
    INT: str = "int"
    FLOAT: str = "float"
    BOOL: str = "bool"


class ParameterIn(str, Enum):
    """参数支持存放的位置"""
    PATH: str = "path"
    QUERY: str = "query"
    HEADER: str = "header"
    COOKIE: str = "cookie"
    REQUEST_BODY = "request_body"


"""
页面端输入的可能是

{
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
      ],
      "responses": { "200": { "description": "ok" } }
    }
  }
}

校验通过后，paths 字段应变成（responses 等会被丢掉，只保留约定字段）：



{
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


完整数据大致：

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


class OpenAPISchema(BaseModel):
    """OpenAPI规范的数据结构"""
    server: str = Field(default="", validate_default=True, description="工具提供者的服务基础地址")
    description: str = Field(
        default="",
        validate_default=True,
        description="工具提供者的描述信息",
        validation_alias=AliasChoices("description", "descriptions"),
    )
    paths: dict[str, dict] = Field(default_factory=dict, validate_default=True, description="工具提供者的路径参数字典")

    @field_validator("server", mode="before")
    def validate_server(cls, server: str) -> str:
        """校验server数据"""
        if server is None or server == "":
            raise ValidationErrorException("server不能为空且为字符串")
        return server

    @field_validator("description", mode="before")
    def validate_description(cls, description: str) -> str:
        """校验description信息"""
        if description is None or description == "":
            raise ValidationErrorException("description不能为空且为字符串")
        return description

    @field_validator("paths", mode="before")
    def validate_paths(cls, paths: dict[str, dict]) -> dict[str, dict]:
        """校验paths信息，涵盖：方法提取，operationId唯一标识，parameters校验"""
        # 1. paths 不为空且类型为字典
        if not paths or not isinstance(paths, dict):
            raise ValidationErrorException("openapi_schema中的paths不能为空且必须是字典")

        # 2. 提取paths里的每一项，并获取元素下的get / post方法对应的值
        methods = ["get", "post"]
        interfaces = []
        extra_paths = {}
        for path, path_item in paths.items():
            for method in methods:
                # 3. 检查是否存在特定的方法并提取信息
                if method in path_item:
                    interfaces.append({
                        "path": path,
                        "method": method,
                        "operation": path_item[method]
                    })
        # 4. 遍历提取到所有接口信息并校验，涵盖operationId唯一标识，parameters参数
        operation_ids = []
        for interface in interfaces:
            # 5. 校验 description / operationId / parameters 字段
            if not isinstance(interface["operation"].get("description"), str):
                raise ValidationErrorException("description不能为空且必须是字符串")
            if not isinstance(interface["operation"].get("operationId"), str):
                raise ValidationErrorException("operationId不能为空且必须是字符串")
            if not isinstance(interface["operation"].get("parameters", []), list):
                raise ValidationErrorException("parameters必须是列表或者为空")
            # 6. 检测 operationId 是否唯一
            operation_id = interface["operation"]["operationId"]
            if operation_id in operation_ids:
                raise ValidationErrorException(f"operationId必须唯一，{operation_id}出现重复")
            operation_ids.append(operation_id)

            # 7. 校验 parameters参数格式是否正确
            for parameter in interface["operation"].get("parameters", []):
                # 8. 校验 name / in / description/ required / type 参数是否存在，并且类型正确
                if not isinstance(parameter.get("name"), str):
                    raise ValidationErrorException("parameter.name参数必须为字符串且不为空")
                if not isinstance(parameter.get("description"), str):
                    raise ValidationErrorException("parameter.description 参数必须为字符串且不为空")
                if not isinstance(parameter.get("required"), bool):
                    raise ValidationErrorException("parameter.required参数必须为布尔值且不为空")
                if (
                        not isinstance(parameter.get("in"), str)
                        or parameter.get("in") not in {item.value for item in ParameterIn}
                ):
                    raise ValidationErrorException(
                        f"parameter.in 参数必须为{'/'.join([item.value for item in ParameterIn])}")
                if (
                        not isinstance(parameter.get("type"), str)
                        or parameter.get("type") not in {item.value for item in ParameterType}
                ):
                    raise ValidationErrorException(
                        f"parameter.type 参数必须为{'/'.join([item.value for item in ParameterType])}")
            # 9. 组装数据并更新（同一路径下 get/post 合并，避免互相覆盖）
            path_key = interface["path"]
            if path_key not in extra_paths:
                extra_paths[path_key] = {}
            extra_paths[path_key][interface["method"]] = {
                "description": interface["operation"]["description"],
                "operationId": operation_id,
                "parameters": [
                    {
                        "name": parameter.get("name"),
                        "in": parameter.get("in"),
                        "description": parameter.get("description"),
                        "required": parameter.get("required"),
                        "type": parameter.get("type")
                    } for parameter in interface["operation"].get("parameters", [])
                ]
            }

        return extra_paths
