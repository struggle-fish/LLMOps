"""
@Time    : 2026/10/27 09:22
@Author  : jzy
@File    : tool_entity.py
"""

from pydantic import BaseModel, Field


class ToolEntity(BaseModel):
    """API 工具实体信息,记录了创建 LangChain 工具所需的配置信息"""
    id: str = Field(default="", description="API 工具提供者对应的 id")
    name: str = Field(default="", description="API 工具名称")
    url: str = Field(default="", description="API 工具发起请求的 URL 地址")
    method: str = Field(default="", description="API 工具发起请求的方法")
    description: str = Field(default="", description="API 工具的描述信息")
    headers: list[dict] = Field(default_factory=list, description="API 工具的请求头信息")
    parameters: list[dict] = Field(default_factory=list, description="API 工具的参数列表信息")