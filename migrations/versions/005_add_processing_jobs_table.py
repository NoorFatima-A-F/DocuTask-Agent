"""add processing_jobs table

Revision ID: 005_add_processing_jobs_table
Revises: 004_add_ai_extractions_table
Create Date: 2026-08-17 22:50:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '005_add_processing_jobs_table'
down_revision: Union[str, None] = '004_add_ai_extractions_table'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'processing_jobs',
        sa.Column('id', sa.Uuid(as_uuid=True), nullable=False),
        sa.Column('document_id', sa.Uuid(as_uuid=True), nullable=False),
        sa.Column('job_type', sa.String(length=50), nullable=False, server_default='DOCUMENT_PIPELINE'),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='QUEUED'),
        sa.Column('priority', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('attempts', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('max_attempts', sa.Integer(), nullable=False, server_default='3'),
        sa.Column('progress', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_error', sa.Text(), nullable=True),
        sa.Column('worker_name', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['document_id'], ['documents.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_processing_jobs_id'), 'processing_jobs', ['id'], unique=False)
    op.create_index(op.f('ix_processing_jobs_document_id'), 'processing_jobs', ['document_id'], unique=False)
    op.create_index(op.f('ix_processing_jobs_status'), 'processing_jobs', ['status'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_processing_jobs_status'), table_name='processing_jobs')
    op.drop_index(op.f('ix_processing_jobs_document_id'), table_name='processing_jobs')
    op.drop_index(op.f('ix_processing_jobs_id'), table_name='processing_jobs')
    op.drop_table('processing_jobs')
