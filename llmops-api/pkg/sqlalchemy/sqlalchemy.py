"""
@Time   : 2026/8/9 08:57
@Author : jzy
@File   : sqlalchemy.py
"""
from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy


class SQLAlchemy(_SQLAlchemy):
    """
    自定义SQLAlchemy类，添加上下文管理器方法
    """

    @contextmanager
    def auto_commit(self):
        """
        上下文管理器，自动提交事务
        """
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
