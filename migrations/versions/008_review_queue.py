"""human review: confidence breakdown, final_json, review_events

Revision ID: 008_review_queue
Revises: 007_extraction_failure_status
Create Date: 2026-11-08 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "008_review_queue"
down_revision: str | None = "007_extraction_failure_status"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table("ai_extractions") as batch:
        batch.add_column(sa.Column("confidence_details", sa.Text(), nullable=True))
        batch.add_column(sa.Column("final_json", sa.Text(), nullable=True))

    op.create_table(
        "review_events",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("extraction_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("reviewer_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("action", sa.String(length=20), nullable=False),
        sa.Column("original_json", sa.Text(), nullable=True),
        sa.Column("corrected_json", sa.Text(), nullable=True),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["extraction_id"], ["ai_extractions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["reviewer_id"], ["users.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_review_events_id", "review_events", ["id"])
    op.create_index("ix_review_events_extraction_id", "review_events", ["extraction_id"])
    op.create_index("ix_review_events_reviewer_id", "review_events", ["reviewer_id"])


def downgrade() -> None:
    op.drop_index("ix_review_events_reviewer_id", table_name="review_events")
    op.drop_index("ix_review_events_extraction_id", table_name="review_events")
    op.drop_index("ix_review_events_id", table_name="review_events")
    op.drop_table("review_events")
    with op.batch_alter_table("ai_extractions") as batch:
        batch.drop_column("final_json")
        batch.drop_column("confidence_details")
