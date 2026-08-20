"""
@Time   : 2026/8/8 10:02
@Author : jzy
@File   : config.py
"""
import os
from typing import Any

from config.default_config import DEFAULT_CONFIG


def _get_env(key: str) -> Any:
    """获取配置类 从环境变量里获取配置项，如果找不到返回默认值"""
    return os.getenv(key, DEFAULT_CONFIG.get(key))


def _get_bool_env(key: str, default: bool = False) -> bool:
    """获取布尔类型的环境变量"""
    value = _get_env(key)
    if value is None:
        return default
    return value.lower() in ("true", "1", "yes")


class Config:
    """基础配置类"""

    def __init__(self):
        # 禁用CSRF保护
        self.WTF_CSRF_ENABLED = _get_bool_env("WTF_CSRF_ENABLED", default=False)

        # 数据库配置
        self.SQLALCHEMY_DATABASE_URI = _get_env("SQLALCHEMY_DATABASE_URI")
        self.SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_size": int(_get_env("SQLALCHEMY_POOL_SIZE") or 30),
            "pool_recycle": int(_get_env("SQLALCHEMY_POOL_RECYCLE") or 3600),
        }
        self.SQLALCHEMY_ECHO = _get_bool_env("SQLALCHEMY_ECHO", default=True)
