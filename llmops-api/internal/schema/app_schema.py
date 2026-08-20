"""
@Time   : 2026/8/8 09:56
@Author : jzy
@File   : app_schema.py
"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class CompletionReq(FlaskForm):
    """基础聊天请求参数校验"""

    query = StringField('query', validators=[
        DataRequired(message="用户的提问不能为空"),
        Length(max=2000, message="用户的提问最大长度是2000")
    ])
