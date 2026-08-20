"""
@Time   : 2026/8/13 15:44
@Author : jzy
@File   : 4.复用提示模版.py
"""

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

full_template = PromptTemplate.from_template(
    """
    {instruction}
    
    
    {example}
    
    
    {start}
    
    """
)

# 描述模板
instruction_prompt = PromptTemplate.from_template("你正在模拟{person}")

# 示例模版
example_prompt = PromptTemplate.from_template("""

    下面是一个交互例子：
    Q: {example_q}
    
    A: {example_a}

""")

# 开始模版

start_prompt = PromptTemplate.from_template("""

    现在你是一个真实的人，请回答用户的问题:
    
    Q:{input}
    
    A:
""")

# 先保留原始输入，再将三个子模板的结果写入最终模板需要的字段。
# 这样可以用 Runnable 管道替代已从新版 LangChain 移除的 PipelinePromptTemplate。
pipeline_prompt = (
    RunnablePassthrough.assign(
        instruction=instruction_prompt,
        example=example_prompt,
        start=start_prompt,
    )
    | full_template
)

# 调用管道生成最终提示词，所有子模板所需的变量都从同一个输入字典中提供。
result = pipeline_prompt.invoke(
    {
        "person": "一个耐心的老师",
        "example_q": "什么是变量？",
        "example_a": "变量是用来保存数据的名称。",
        "input": "什么是函数？",
    }
)

# PromptTemplate 返回 PromptValue，转换成字符串后便于直接查看最终内容。
print(result.to_string())
