"""
@Time   : 2026/8/7 15:48
@Author : jzy
@File   : app_handler.py
"""
import os

from dataclasses import dataclass
from uuid import UUID
from flask import request
from injector import inject
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from openai import OpenAI
from langchain_core.output_parsers import StrOutputParser

from internal.exception import FailException
from internal.schema.app_schema import CompletionReq
from internal.service import AppService
from pkg.response import success_json, validate_error_json, success_message


@inject
@dataclass
class AppHandler:
    """应用控制器"""
    app_service: AppService

    def create_app(self):
        """调用服务创建新的app记录"""
        app = self.app_service.create_app()
        return success_message(f"创建应用成功, id为: {app.id}")

    def get_app(self, id: UUID):
        app = self.app_service.get_app(id)
        return success_message(f"获取应用成功, id为: {app.id}, name为: {app.name}")

    def update_app(self, id: UUID):
        app = self.app_service.update_app(id)
        if not app:
            return success_message(f"更新应用失败, id为: {id}")
        return success_message(f"更新应用成功, id为: {app.id}, name为: {app.name}")

    def delete_app(self, id: UUID):
        app = self.app_service.delete_app(id)
        if not app:
            return success_message(f"删除应用失败, id为: {id}")
        return success_message(f"删除应用成功, id为: {app.id}, name为: {app.name}")

    def debug(self, app_id: UUID):
        """聊天接口"""
        # 1.提取从接口中获取的输入
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(req.errors)

        """
        # 原始调用
        # query = request.json.get("query")
        # 2.构建openai客户端，发起请求
        # client = OpenAI(
        #     api_key=os.getenv("OPENAI_API_KEY"),
        #     base_url=os.getenv("OPENAI_BASE_URL"),
        # )
        
        # 3.得到请求响应，然后将openai的响应返回给前端
        # completion = client.chat.completions.create(
        #     model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
        #     messages=[
        #         {"role": "system", "content": "你是openai开发的聊天机器人，请根据用户的输入回复对应的消息"},
        #         {"role": "user", "content": query},
        #     ],
        # )

        # content = completion.choices[0].message.content
        """
        prompt = ChatPromptTemplate.from_template("{query}")
        llm = ChatOpenAI()
        parser = StrOutputParser()

        # 构建链
        chain = prompt | llm | parser

        content = chain.invoke({"query": req.query.data})

        return success_json({"content": content})

    def ping(self):
        # 处理ping请求的逻辑
        # return {"ping": "pong"}
        raise FailException("ping请求失败")
