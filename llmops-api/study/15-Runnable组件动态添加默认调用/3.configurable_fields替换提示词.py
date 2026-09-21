"""
@Time   : 2026/8/28 14:12
@Author : jzy
@File   : 3.configurable_fields替换提示词.py
"""

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import ConfigurableField

prompt = PromptTemplate.from_template("请写一篇关于{subject}主题的冷笑话").configurable_fields(
    template=ConfigurableField(id="prompt_template")
)

content = prompt.invoke(
    {
        "subject": "程序员"
    },
    config={"configurable": {"prompt_template": "请写一个关于{subject}的藏头诗"}}
).to_string()

print(content)
