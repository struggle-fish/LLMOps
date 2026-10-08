"""
@Time   : 2026/10/7 18:48
@Author : jzy
@File   : 测试.py
"""
import os
import dotenv
from langchain_community.utilities import SerpAPIWrapper

dotenv.load_dotenv()
wrapper = SerpAPIWrapper(serpapi_api_key=os.getenv("SERPAPI_API_KEY"))
result = wrapper.run("马拉松的世界记录是多少")
print(result)
