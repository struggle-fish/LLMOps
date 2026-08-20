"""
@Time   : 2026/8/7 16:14
@Author : jzy
@File   : app.py
"""
import dotenv
from flask_migrate import Migrate

from pkg.sqlalchemy import SQLAlchemy

from injector import Injector

from config import Config
from internal.router import Router
from internal.server import Http
from .module import ExtensionModule

dotenv.load_dotenv()  # 加载.env文件中的环境变量
conf = Config()  # 创建配置类实例

injector = Injector([ExtensionModule])  # 创建依赖注入器实例

app = Http(
    __name__,
    conf=conf,
    db=injector.get(SQLAlchemy),
    migrate=injector.get(Migrate),  # 这里的migrate参数需要传入实际的Migrate实例
    router=injector.get(Router))  # 这里的router参数需要传入实际的Router实例

# 如果当前文件是被执行的，那么就开启debug模式运行Flask应用
if __name__ == '__main__':
    app.run()
