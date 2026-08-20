"""
@Time   : 2026/8/8 10:52
@Author : jzy
@File   : http_code.py
"""
from enum import Enum


class HttpCode(str, Enum):
    """HTTP基础业务状态码"""

    SUCCESS = "success"  # 成功状态
    FAIL = "fail"  # 失败状态
    NOT_FOUND = "not_found"  # 未找到资源
    UNAUTHORIZED = "unauthorized"  # 未授权访问
    FORBIDDEN = "forbidden"  # 禁止访问
    VALIDATION_ERROR = "validation_error"  # 数据验证错误
