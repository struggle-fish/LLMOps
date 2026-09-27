"""
@Time   : 2026/9/24 11:54
@Author : jzy
@File   : 1.问答转换器示例.py
"""
import dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document

# 加载环境变量
dotenv.load_dotenv()


# 定义结构化输出模型，替代 DoctranQATransformer
class QAPair(BaseModel):
    question: str = Field(description="基于文档生成的问题")
    answer: str = Field(description="文档对应的答案")


class QAOutput(BaseModel):
    questions_and_answers: list[QAPair] = Field(description="问答对列表")


# 初始化大模型
llm = ChatOpenAI(model="gpt-5.4-mini", temperature=0)
llm_structured = llm.with_structured_output(QAOutput)

# 1.构建文档列表
page_content = """机密文件 - 仅供内部使用
日期：2023年7月1日
主题：各种话题的更新和讨论
亲爱的团队，
希望这封邮件能找到你们一切安好。在这份文件中，我想向你们提供一些重要的更新，并讨论需要我们关注的各种话题。请将此处包含的信息视为高度机密。
安全和隐私措施
作为我们不断致力于确保客户数据安全和隐私的一部分，我们已在所有系统中实施了强有力的措施。我们要赞扬IT部门的John Doe（电子邮件：john.doe@example.com）在增强我们网络安全方面的勤奋工作。未来，我们提醒每个人严格遵守我们的数据保护政策和准则。此外，如果您发现任何潜在的安全风险或事件，请立即向我们专门的团队报告，联系邮箱为security@example.com。
人力资源更新和员工福利
最近，我们迎来了几位为各自部门做出重大贡献的新团队成员。我要表扬Jane Smith（社保号：049-45-5928）在客户服务方面的出色表现。Jane一直受到客户的积极反馈。此外，请记住我们的员工福利计划的开放报名期即将到来。如果您有任何问题或需要帮助，请联系我们的人力资源代表Michael Johnson（电话：418-492-3850，电子邮件：michael.johnson@example.com）。
营销倡议和活动
我们的营销团队一直在积极制定新策略，以提高品牌知名度并推动客户参与。我们要感谢Sarah Thompson（电话：415-555-1234）在管理我们的社交媒体平台方面的杰出努力。Sarah在过去一个月内成功将我们的关注者基数增加了20%。此外，请记住7月15日即将举行的产品发布活动。我们鼓励所有团队成员参加并支持我们公司的这一重要里程碑。
研发项目
在追求创新的过程中，我们的研发部门一直在为各种项目不懈努力。我要赞扬David Rodriguez（电子邮件：david.rodriguez@example.com）在项目负责人角色中的杰出工作。David对我们尖端技术的发展做出了重要贡献。此外，我们希望每个人在7月10日定期举行的研发头脑风暴会议上分享他们的想法和建议，以开展潜在的新项目。
请将此文档中的信息视为最机密，并确保不与未经授权的人员分享。如果您对讨论的话题有任何疑问或顾虑，请随时直接联系我。
感谢您的关注，让我们继续共同努力实现我们的目标。
此致，
Jason Fan
联合创始人兼首席执行官
Psychic
jason@psychic.dev"""

documents = [Document(page_content=page_content)]

# 2. 生成问答对，效果等价 DoctranQATransformer
result = llm_structured.invoke(f"""
阅读下面文档，提取文档关键信息，生成问答对。
输出 questions_and_answers 数组，每个元素包含 question 和 answer。
文档内容：
{documents[0].page_content}
""")

# 把问答对写入 document metadata，和原代码保持一致
documents[0].metadata["questions_and_answers"] = result.questions_and_answers

# 3.输出内容，和原来打印逻辑完全一样
for qa in documents[0].metadata.get("questions_and_answers", []):
    print("问答数据:", qa.model_dump())
