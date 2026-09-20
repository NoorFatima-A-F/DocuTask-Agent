"""add ai_extractions table

Revision ID: 004_add_ai_extractions_table
Revises: 003_add_extracted_text_table
Create Date: 2026-08-17 22:45:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '004_add_ai_extractions_table'
down_revision: Union[str, None] = '003_add_extracted_text_table'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'ai_extractions',
        sa.Column('id', sa.Uuid(as_uuid=True), nullable=False),
        sa.Column('document_id', sa.Uuid(as_uuid=True), nullable=False),
        sa.Column('document_type', sa.String(length=50), nullable=False),
        sa.Column('provider', sa.String(length=50), nullable=False),
        sa.Column('model', sa.String(length=50), nullable=False),
        sa.Column('raw_response', sa.Text(), nullable=False),
        sa.Column('structured_json', sa.Text(), nullable=False),
        sa.Column('prompt_version', sa.String(length=20), nullable=False, server_default='v1.0'),
        sa.Column('processing_time_ms', sa.Integer(), nullable=False),
        sa.Column('input_tokens', sa.Integer(), nullable=False),
        sa.Column('output_tokens', sa.Integer(), nullable=False),
        sa.Column('estimated_cost', sa.Float(), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['document_id'], ['documents.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ai_extractions_id'), 'ai_extractions', ['id'], unique=False)
    op.create_index(op.f('ix_ai_extractions_document_id'), 'ai_extractions', ['document_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_ai_extractions_document_id'), table_name='ai_extractions')
    op.drop_index(op.f('ix_ai_extractions_id'), table_name='ai_extractions')
    op.drop_table('ai_extractions')
