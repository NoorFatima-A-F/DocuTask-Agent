"""
Vector Search Readiness SQLAlchemy ORM Entities.
Defines DocumentEmbedding table supporting HNSW vector indexes, embedding provider, model, dimension, and timestamps.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, UUIDMixin


class DocumentEmbedding(Base, UUIDMixin):
    """DocumentEmbedding entity supporting pgvector HNSW semantic vector retrieval."""

    __tablename__ = "document_embeddings"

    document_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("documents.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    chunk_text: Mapped[str] = mapped_column(Text, nullable=False)
    
    embedding_provider: Mapped[str] = mapped_column(String(50), nullable=False, default="gemini")
    embedding_model: Mapped[str] = mapped_column(String(100), nullable=False, default="text-embedding-004")
    embedding_dim: Mapped[int] = mapped_column(Integer, nullable=False, default=768)
    
    # Vector payload stored as serialized string / pgvector payload
    vector_payload: Mapped[str] = mapped_column(Text, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True,
        nullable=False
    )
