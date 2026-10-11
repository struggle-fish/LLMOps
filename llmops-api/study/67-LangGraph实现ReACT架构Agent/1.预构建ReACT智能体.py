"""
@Time   : 2026/10/10 10:23
@Author : jzy
@File   : 1.预构建ReACT智能体.py
"""
import dotenv
from langchain_community.tools import GoogleSerperRun
from langchain_community.tools.openai_dalle_image_generation import OpenAIDALLEImageGenerationTool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
# ========== 新版导入，替换原来 langgraph.prebuilt.create_react_agent ==========
from langchain.agents import create_agent

dotenv.load_dotenv()


class GoogleSerperArgsSchema(BaseModel):
    query: str = Field(description="执行谷歌搜索的查询语句")


class DallEArgsSchema(BaseModel):
    query: str = Field(description="输入应该是生成图像的文本提示(prompt)")


# 1.定义工具与工具列表
google_serper = GoogleSerperRun(
    name="google_serper",
    description=(
        "一个低成本的谷歌搜索API。"
        "当你需要回答有关时事的问题时，可以调用该工具。"
        "该工具的输入是搜索查询语句。"
    ),
    args_schema=GoogleSerperArgsSchema,
    api_wrapper=GoogleSerperAPIWrapper(),
)
dalle = OpenAIDALLEImageGenerationTool(
    name="openai_dalle",
    api_wrapper=DallEAPIWrapper(model="gpt-image-2"),
    args_schema=DallEArgsSchema,
)
tools = [google_serper, dalle]

# 2.创建大语言模型
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 3.新版：create_agent，替换旧版 create_react_agent
agent = create_agent(model=model, tools=tools)

# 4.调用智能体，invoke 写法不变
result = agent.invoke({"messages": [("human", "请帮我绘制一幅鲨鱼在天上飞的图片")]})

# 美化输出，方便看结果
print(result["messages"][-1].content)
