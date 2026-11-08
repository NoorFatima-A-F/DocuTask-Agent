"""add user roles and is_verified fields

Revision ID: 006_add_user_roles_and_verified
Revises: 005_add_processing_jobs_table
Create Date: 2026-08-17 23:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "006_add_user_roles_and_verified"
down_revision: str | None = "005_add_processing_jobs_table"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("users", sa.Column("role", sa.String(length=20), nullable=False, server_default="user"))
    op.add_column("users", sa.Column("is_verified", sa.Boolean(), nullable=False, server_default="0"))


def downgrade() -> None:
    op.drop_column("users", "is_verified")
    op.drop_column("users", "role")
