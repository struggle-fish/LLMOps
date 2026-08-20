"""
@Time   : 2026/8/8 17:24
@Author : jzy
@File   : app_service.py
"""
import uuid
from dataclasses import dataclass
from pkg.sqlalchemy import SQLAlchemy
from injector import inject
from internal.model import App


@inject
@dataclass
class AppService:
    """
    应用服务类
    """

    db: SQLAlchemy

    def create_app(self) -> App:
        """
        创建应用
        """
        # 1.创建模型的实体类、
        with self.db.auto_commit():
            app = App(
                name="测试机器人",
                account_id=uuid.uuid4(),
                icon="",
                description="这是一个测试机器人",
            )
            # 2.将实体类添加到session会话中
            self.db.session.add(app)
        return app

    def get_app(self, id: uuid.UUID) -> App:
        """
        根据id获取应用
        """
        app = self.db.session.query(App).get(id)
        return app

    def update_app(self, id: uuid.UUID) -> App:
        """
        根据id更新应用
        """
        with self.db.auto_commit():
            app = self.get_app(id)
            if not app:
                return None
            app.name = "更新后的测试机器人"

        return app

    def delete_app(self, id: uuid.UUID) -> App:
        """
        根据id删除应用
        """
        with self.db.auto_commit():
            app = self.get_app(id)
            self.db.session.delete(app)
        return app
