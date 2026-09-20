"""add extracted_text table

Revision ID: 003_add_extracted_text_table
Revises: 002_add_documents_table
Create Date: 2026-08-17 22:40:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '003_add_extracted_text_table'
down_revision: Union[str, None] = '002_add_documents_table'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'extracted_texts',
        sa.Column('id', sa.Uuid(as_uuid=True), nullable=False),
        sa.Column('document_id', sa.Uuid(as_uuid=True), nullable=False),
        sa.Column('page_number', sa.Integer(), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=False),
        sa.Column('processing_method', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['document_id'], ['documents.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_extracted_texts_id'), 'extracted_texts', ['id'], unique=False)
    op.create_index(op.f('ix_extracted_texts_document_id'), 'extracted_texts', ['document_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_extracted_texts_document_id'), table_name='extracted_texts')
    op.drop_index(op.f('ix_extracted_texts_id'), table_name='extracted_texts')
    op.drop_table('extracted_texts')
