"""
@Time   : 2026/10/8 11:12
@Author : jzy
@File   : 2.LLM文生图应用.py
"""
import dotenv
from langchain_community.tools.openai_dalle_image_generation import OpenAIDALLEImageGenerationTool
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

dalle = OpenAIDALLEImageGenerationTool(api_wrapper=DallEAPIWrapper(model="gpt-image-2"))

llm = ChatOpenAI(model="gpt-4o")
llm_with_tools = llm.bind_tools([dalle], tool_choice="openai_dalle")

chain = llm_with_tools | (lambda msg: msg.tool_calls[0]["args"]) | dalle

print(chain.invoke("帮我绘制一张老爷爷爬山的图片"))
