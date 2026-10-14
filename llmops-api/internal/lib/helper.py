"""
@Time   : 2026/10/13 10:04
@Author : jzy
@File   : helper.py
"""

import importlib
from typing import Any


def dynamic_import(module_name: str, symbol_name: str) -> Any:
    """动态导入模块中的函数"""
    module = importlib.import_module(module_name)
    return getattr(module, symbol_name)


def add_attribute(attr_name: str, attr_value: Any):
    """装饰器函数：动态添加属性，第一个参数为属性名字，第二个参数为属性值"""

    def decorator(func: Any):
        setattr(func, attr_name, attr_value)
        return func

    return decorator
