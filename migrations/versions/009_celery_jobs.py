"""celery jobs: idempotency key, document type, error code; drop in-memory-queue columns

Revision ID: 009_celery_jobs
Revises: 008_review_queue
Create Date: 2026-11-08 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "009_celery_jobs"
down_revision: str | None = "008_review_queue"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table("processing_jobs") as batch:
        batch.add_column(sa.Column("document_type", sa.String(length=50), nullable=False, server_default="generic"))
        batch.add_column(sa.Column("idempotency_key", sa.String(length=64), nullable=True))
        batch.add_column(sa.Column("error_code", sa.String(length=64), nullable=True))
        batch.create_unique_constraint("uq_processing_jobs_idempotency_key", ["idempotency_key"])
        batch.drop_column("job_type")
        batch.drop_column("priority")
        batch.drop_column("progress")
        batch.drop_column("worker_name")


def downgrade() -> None:
    with op.batch_alter_table("processing_jobs") as batch:
        batch.add_column(sa.Column("worker_name", sa.String(length=100), nullable=True))
        batch.add_column(sa.Column("progress", sa.Float(), nullable=False, server_default="0.0"))
        batch.add_column(sa.Column("priority", sa.Integer(), nullable=False, server_default="1"))
        batch.add_column(
            sa.Column("job_type", sa.String(length=50), nullable=False, server_default="DOCUMENT_PIPELINE")
        )
        batch.drop_constraint("uq_processing_jobs_idempotency_key", type_="unique")
        batch.drop_column("error_code")
        batch.drop_column("idempotency_key")
        batch.drop_column("document_type")
