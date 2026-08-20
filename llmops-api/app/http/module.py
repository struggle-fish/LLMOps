"""
@Time   : 2026/8/8 16:54
@Author : jzy
@File   : module.py
"""
from flask_migrate import Migrate
from pkg.sqlalchemy import SQLAlchemy
from injector import Binder, Module

from internal.extension.database_extension import db
from internal.extension.migrate_extension import migrate


class ExtensionModule(Module):
    """依赖注入模块"""

    def configure(self, binder: Binder) -> None:
        # 绑定数据库实例
        binder.bind(SQLAlchemy, to=db)
        binder.bind(Migrate, to=migrate)
