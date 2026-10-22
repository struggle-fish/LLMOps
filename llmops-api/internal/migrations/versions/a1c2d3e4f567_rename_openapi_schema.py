"""Rename API tool provider schema column without losing existing data.

Revision ID: a1c2d3e4f567
Revises: 8a49bd51e35a
"""
from alembic import op
import sqlalchemy as sa

revision = 'a1c2d3e4f567'
down_revision = '8a49bd51e35a'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'api_tool_provider', 'openai_schema',
        new_column_name='openapi_schema', existing_type=sa.Text(),
        existing_nullable=False,
    )


def downgrade():
    op.alter_column(
        'api_tool_provider', 'openapi_schema',
        new_column_name='openai_schema', existing_type=sa.Text(),
        existing_nullable=False,
    )
