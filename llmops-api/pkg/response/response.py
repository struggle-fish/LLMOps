"""
@Time   : 2026/8/8 10:54
@Author : jzy
@File   : response.py
"""
from dataclasses import field, dataclass
from typing import Any

from flask import Response, jsonify

from .http_code import HttpCode


@dataclass
class Response:
    """统一响应类"""
    code: HttpCode = HttpCode.SUCCESS  # 响应状态码
    msg: str = ""  # 响应消息
    data: Any = field(default_factory=dict)  # 响应数据


def json(data: Response = None):
    """基础的响应接口"""
    return jsonify(data), 200


def success_json(data: Any = None):
    """返回成功响应的JSON格式"""
    return json(Response(code=HttpCode.SUCCESS, msg="", data=data))


def fail_json(data: Any = None):
    """返回失败响应的JSON格式"""
    return json(Response(code=HttpCode.FAIL, msg="", data=data))


def validate_error_json(errors: dict = None):
    """返回数据验证错误响应的JSON格式"""
    first_key = next(iter(errors))
    msg = errors[first_key][0] if errors and first_key in errors else ""

    return json(Response(code=HttpCode.VALIDATION_ERROR, msg=msg, data=errors))


def message(code: HttpCode = None, msg: str = ""):
    """返回消息响应的JSON格式, 固定返回消息提示，数据固定为空字典"""
    return json(Response(code=code, msg=msg, data={}))


def success_message(msg: str = ""):
    """返回成功消息响应的JSON格式"""
    return message(code=HttpCode.SUCCESS, msg=msg)


def fial_message(msg: str = ""):
    """返回失败消息响应的JSON格式"""
    return message(code=HttpCode.FAIL, msg=msg)


def not_found_message(msg: str = ""):
    """返回未找到资源消息响应的JSON格式"""
    return message(code=HttpCode.NOT_FOUND, msg=msg)


def unauthorized_message(msg: str = ""):
    """返回未授权访问消息响应的JSON格式"""
    return message(code=HttpCode.UNAUTHORIZED, msg=msg)


def forbidden_message(msg: str = ""):
    """返回禁止访问消息响应的JSON格式"""
    return message(code=HttpCode.FORBIDDEN, msg=msg)
