"""
@Time   : 2026/10/13 21:51
@Author : jzy
@File   : gptimage2.py
"""

from langchain_community.tools.openai_dalle_image_generation import OpenAIDALLEImageGenerationTool
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool

from internal.lib.helper import add_attribute


# from internal.lib.helper import add_attribute


class GptImage2ArgsSchema(BaseModel):
    query: str = Field(description="输入应该是生成图像的文本提示(prompt)")


@add_attribute("args_schema", GptImage2ArgsSchema)
def gptimage2(**kwargs) -> BaseTool:
    """返回gpt-image-2绘图的LangChain工具"""
    return OpenAIDALLEImageGenerationTool(
        api_wrapper=DallEAPIWrapper(model="gpt-image-2", **kwargs),
        args_schema=GptImage2ArgsSchema,
    )
