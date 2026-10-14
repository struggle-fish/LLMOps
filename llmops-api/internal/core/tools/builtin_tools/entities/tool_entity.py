"""
@Time   : 2026/10/13 09:45
@Author : jzy
@File   : tool_entity.py
"""
from enum import Enum
from typing import Optional, Any

from pydantic import BaseModel, Field


class ToolParamType(str, Enum):
    """工具参数类型枚举类"""
    STRING = "string"  # 字符串类型
    NUMBER = "number"  # 数字类型
    FLOAT = "float"  # 浮点数类型
    BOOLEAN = "boolean"  # 布尔类型
    SELECT = "select"  # 下拉选择类型


class ToolParam(BaseModel):
    """工具参数类，存储的信息是类似google_serper.yaml里的信息"""
    name: str  # 参数的名字
    label: str  # 参数的标签，给前端看的
    type: ToolParamType  # 参数的类型
    required: bool = False  # 参数是否必填
    default: Optional[Any] = None  # 参数的默认值
    min: Optional[float] = None  # 参数的最小值
    max: Optional[float] = None  # 参数的最大值
    options: list[dict[str, Any]] = Field(default_factory=list)  # 下拉菜单选项列表


class ToolEntity(BaseModel):
    """工具实体类，存储的信息是类似google_serper.yaml里的信息"""
    name: str  # 工具的名字
    label: str  # 工具的标签，给前端看的
    description: str  # 工具的描述
    params: list[ToolParam] = Field(default_factory=list)  # 工具的参数列表
