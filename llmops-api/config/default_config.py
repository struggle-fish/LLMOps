"""
@Time   : 2026/8/8 16:38
@Author : jzy
@File   : default_config.py
"""

# 应用默认配置项

DEFAULT_CONFIG = {
    # wft默认配置
    "WTF_CSRF_ENABLED": "False",

    # 数据库配置
    "SQLALCHEMY_DATABASE_URI": "",
    "SQLALCHEMY_POOL_SIZE": 30,
    "SQLALCHEMY_POOL_TIMEOUT": 3600,
    "SQLALCHEMY_ECHO": "True",
}
