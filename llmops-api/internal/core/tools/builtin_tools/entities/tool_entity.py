"""
@Time   : 2026/10/13 09:45
@Author : jzy
@File   : tool_entity.py
"""

from pydantic import BaseModel


class ToolEntity(BaseModel):
    """工具实体类，存储的信息是类似google_serper.yaml里的信息"""
    name: str  # 工具的名字
    label: str  # 工具的标签，给前端看的
    description: str  # 工具的描述
    params: list = []  # 工具的参数列表
