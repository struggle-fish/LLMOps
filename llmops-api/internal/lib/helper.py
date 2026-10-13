"""
@Time   : 2026/10/13 10:04
@Author : jzy
@File   : helper.py
"""

import imaplib
from typing import Any


def dynamic_import(module_name: str, symbol_name: str) -> Any:
    """动态导入模块中的函数"""
    module = imaplib.import_module(module_name)
    return getattr(module, symbol_name)
