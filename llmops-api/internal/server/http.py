"""
@Time   : 2026/8/7 16:12
@Author : jzy
@File   : http.py
"""
import os

from flask import Flask
from flask_migrate import Migrate

from config import Config
from internal.exception import CustomException
from internal.router import Router
from pkg.response import json, Response, HttpCode
from pkg.sqlalchemy import SQLAlchemy

from internal.model import App


class Http(Flask):
    """HTTP服务器"""

    def __init__(
            self,
            *args,
            conf: Config,
            db: SQLAlchemy,
            migrate: Migrate,
            router: Router,
            **kwargs):
        super().__init__(*args, **kwargs)
        # 加载配置类
        self.config.from_object(conf)

        # 异常错误处理
        self.register_error_handler(Exception, self._register_error_handlers)

        # flask扩展
        db.init_app(self)
        migrate.init_app(self, db, 'internal/migrations')
        # 自动创建数据库表
        # with self.app_context():
        #     _ = App()
        #     db.create_all()

        # 注册应用路由
        router.register_route(self)

    def _register_error_handlers(self, error: Exception):
        """统一处理异常"""
        # 1.异常是否是自定义异常，如果是提取message和code
        if isinstance(error, CustomException):
            return json(
                Response(
                    code=error.code,
                    message=error.message,
                    data=error.data if error.data is not None else {}
                )
            )
        # 2.如果不是自定义异常，可能是程序，数据库异常，也可以提取信息设置为Fail状态码
        if self.debug or os.getenv("FLASK_ENV") == "development":
            """开发环境下直接抛出异常，方便调试"""
            raise error
        else:
            """生产环境"""
            return json(
                Response(
                    code=HttpCode.FAIL,
                    message=str(error),
                    data={}
                )
            )
