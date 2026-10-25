"""
@Time   : 2026/10/18 14:16
@Author : jzy
@File   : api_tool.py
"""
import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    UUID,
    String,
    Text,
    DateTime,
    PrimaryKeyConstraint,
    Index,
)
from sqlalchemy.dialects.postgresql import JSONB

from internal.extension.database_extension import db


class ApiToolProvider(db.Model):
    """API 工具提供者模型"""

    __tablename__ = "api_tool_provider"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_api_tool_provider_id"),
        Index("idx_api_tool_provider_account_id_name", "account_id", "name"),
    )

    id = Column(UUID, default=uuid.uuid4, nullable=False)
    account_id = Column(UUID, default=uuid.uuid4, nullable=False)
    name = Column(String(255), default="", nullable=False)
    icon = Column(String(255), default="", nullable=False)
    description = Column(Text, default="", nullable=False)
    openapi_schema = Column(Text, default="", nullable=False)
    headers = Column(JSONB, default=lambda: [], nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False,
    )
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    @property
    def tools(self) -> list["ApiTool"]:
        return db.session.query(ApiTool).filter_by(provider_id = self.id).all()



class ApiTool(db.Model):
    """API 工具模型"""

    __tablename__ = "api_tool"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_api_tool_id"),
        Index("idx_api_tool_account_id", "account_id"),
        Index("idx_api_tool_provider_id_name", "provider_id", "name"),
    )

    id = Column(UUID, default=uuid.uuid4, nullable=False)
    account_id = Column(UUID, default=uuid.uuid4, nullable=False)
    provider_id = Column(UUID, default=uuid.uuid4, nullable=False)
    name = Column(String(255), default="", nullable=False)
    description = Column(Text, default="", nullable=False)
    url = Column(String(255), default="", nullable=False)
    method = Column(String(255), default="", nullable=False)
    parameters = Column(JSONB, default=lambda: [], nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False,
    )
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    @property
    def provider(self) -> "ApiToolProvider":
        """只读属性，返回当前工具关联/归属的工具提供者信息"""
        return db.session.query(ApiToolProvider).get(self.provider_id)
