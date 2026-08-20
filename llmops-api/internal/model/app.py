"""
@Time   : 2026/8/8 17:09
@Author : jzy
@File   : app.py
"""
import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    UUID, String, Text, DateTime, PrimaryKeyConstraint, Index
)

from internal.extension.database_extension import db


class App(db.Model):
    """AI应用基础模型类"""

    __tablename__ = "app"
    __table_args__ = (
        # 设置主键约束和索引
        PrimaryKeyConstraint("id", name="pk_app_id"),
        Index("idx_app_account_id", "account_id")
    )

    id = Column(UUID, default=uuid.uuid4, nullable=False)
    account_id = Column(UUID, nullable=False)
    name = Column(String(255), default="", nullable=False)
    icon = Column(String(255), default="", nullable=False)
    description = Column(Text, default="", nullable=False)
    status = Column(String(255), default="", nullable=False)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
