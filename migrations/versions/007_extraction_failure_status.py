"""extraction status, typed failures, nullable confidence

Adds ``status``/``error_code``/``error_message`` to ``ai_extractions`` so failed
extractions are persisted as FAILED rows instead of fabricated results, and makes
``structured_json``, ``raw_response``, ``confidence`` and ``estimated_cost`` nullable.
``extracted_texts.confidence`` becomes nullable (no guessed OCR confidence).

Revision ID: 007_extraction_failure_status
Revises: 006_add_user_roles_and_verified
Create Date: 2026-11-08 00:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "007_extraction_failure_status"
down_revision: Union[str, None] = "006_add_user_roles_and_verified"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("ai_extractions") as batch:
        batch.add_column(sa.Column("status", sa.String(length=20), nullable=False, server_default="COMPLETED"))
        batch.add_column(sa.Column("error_code", sa.String(length=50), nullable=True))
        batch.add_column(sa.Column("error_message", sa.Text(), nullable=True))
        batch.alter_column("raw_response", existing_type=sa.Text(), nullable=True)
        batch.alter_column("structured_json", existing_type=sa.Text(), nullable=True)
        batch.alter_column("estimated_cost", existing_type=sa.Float(), nullable=True)
        batch.alter_column("confidence", existing_type=sa.Float(), nullable=True, server_default=None)
        batch.create_index("ix_ai_extractions_status", ["status"], unique=False)

    with op.batch_alter_table("extracted_texts") as batch:
        batch.alter_column("confidence", existing_type=sa.Float(), nullable=True)


def downgrade() -> None:
    op.execute("DELETE FROM ai_extractions WHERE structured_json IS NULL OR confidence IS NULL")
    op.execute("UPDATE ai_extractions SET raw_response = '' WHERE raw_response IS NULL")
    op.execute("UPDATE ai_extractions SET estimated_cost = 0 WHERE estimated_cost IS NULL")
    op.execute("UPDATE extracted_texts SET confidence = 0 WHERE confidence IS NULL")

    with op.batch_alter_table("extracted_texts") as batch:
        batch.alter_column("confidence", existing_type=sa.Float(), nullable=False)

    with op.batch_alter_table("ai_extractions") as batch:
        batch.drop_index("ix_ai_extractions_status")
        batch.alter_column("confidence", existing_type=sa.Float(), nullable=False, server_default="1.0")
        batch.alter_column("estimated_cost", existing_type=sa.Float(), nullable=False)
        batch.alter_column("structured_json", existing_type=sa.Text(), nullable=False)
        batch.alter_column("raw_response", existing_type=sa.Text(), nullable=False)
        batch.drop_column("error_message")
        batch.drop_column("error_code")
        batch.drop_column("status")
