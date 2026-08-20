"""
@Time   : 2026/8/7 15:53
@Author : jzy
@File   : router.py
"""
from dataclasses import dataclass

from flask import Flask, Blueprint
from injector import inject

from internal.handler import AppHandler


@inject
@dataclass
class Router:
    """路由器"""
    app_handler: AppHandler

    def register_route(self, app: Flask):
        """注册路由"""
        # 1. 创建一个蓝图
        bp = Blueprint('llmops', __name__, url_prefix='')

        # 2. 将url与对应的控制器方法做绑定
        # bp.add_url_rule('/ping', view_func=self.app_handler.ping, methods=['GET'])
        bp.add_url_rule('/apps/<uuid:app_id>/debug', view_func=self.app_handler.debug, methods=['POST'])

        # bp.add_url_rule('/app', view_func=self.app_handler.create_app, methods=['POST'])
        # bp.add_url_rule('/app/<uuid:id>', view_func=self.app_handler.get_app, methods=['GET'])
        # bp.add_url_rule('/app/<uuid:id>', view_func=self.app_handler.update_app, methods=['POST'])
        # bp.add_url_rule('/app/<uuid:id>/delete', view_func=self.app_handler.delete_app, methods=['POST'])

        # 3. 将蓝图注册到Flask应用中
        app.register_blueprint(bp)
