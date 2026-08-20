"""
@Time   : 2026/8/8 12:41
@Author : jzy
@File   : exception.py
"""
from dataclasses import field
from typing import Any

from pkg.response import HttpCode


class CustomException(Exception):
    """自定义异常类"""

    code: HttpCode = HttpCode.FAIL  # 默认状态码为失败
    message: str = ""  # 默认错误信息
    data: Any = field(default_factory=dict)  # 默认数据为空字典

    def __init__(self, message: str = None, data: Any = None):
        super().__init__()
        self.message = message
        self.data = data


class FailException(CustomException):
    """失败异常"""
    pass


class NotFoundException(CustomException):
    """未找到异常"""
    code = HttpCode.NOT_FOUND


class UnauthorizedException(CustomException):
    """未授权异常"""
    code = HttpCode.UNAUTHORIZED


class ForbiddenException(CustomException):
    """禁止访问异常"""
    code = HttpCode.FORBIDDEN


class ValidationErrorException(CustomException):
    """数据验证错误异常"""
    code = HttpCode.VALIDATION_ERROR
