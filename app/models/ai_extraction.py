"""
AIExtraction SQLAlchemy ORM Model.
Stores structured LLM extraction outputs, raw responses, token counts, costs, and performance statistics.
"""

import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, UUIDMixin

if TYPE_CHECKING:
    from app.models.document import Document


class AIExtraction(Base, UUIDMixin):
    """AIExtraction database entity representation."""

    __tablename__ = "ai_extractions"

    document_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("documents.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    document_type: Mapped[str] = mapped_column(String(50), nullable=False)
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(50), nullable=False)
    raw_response: Mapped[str] = mapped_column(Text, nullable=False)
    structured_json: Mapped[str] = mapped_column(Text, nullable=False)  # Stored as JSON string
    prompt_version: Mapped[str] = mapped_column(String(20), default="v1.0", nullable=False)
    processing_time_ms: Mapped[int] = mapped_column(Integer, nullable=False)
    input_tokens: Mapped[int] = mapped_column(Integer, nullable=False)
    output_tokens: Mapped[int] = mapped_column(Integer, nullable=False)
    estimated_cost: Mapped[float] = mapped_column(Float, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationship
    document: Mapped["Document"] = relationship("Document", back_populates="ai_extractions")

    def __repr__(self) -> str:
        return f"<AIExtraction(id={self.id}, document_id={self.document_id}, type='{self.document_type}', provider='{self.provider}')>"
