"""
@Time   : 2026/10/19 23:00
@Author : jzy
@File   : schema.py
"""
from typing import Any

from wtforms import Field


class ListField(Field):
    """自定义List字段，用户存储列表型数据"""
    data: list = None

    def process_formdata(self, valuelist):
        if valuelist is not None and isinstance(valuelist, list):
            self.data = valuelist

    def _value(self):
        return self.data if self.data else []
