"""
AIExtraction SQLAlchemy ORM Model.
Stores structured LLM extraction outputs, raw responses, token counts, costs, and performance statistics.
"""

import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, UUIDMixin

if TYPE_CHECKING:
    from app.models.document import Document


class AIExtraction(Base, UUIDMixin):
    """AIExtraction database entity representation."""

    __tablename__ = "ai_extractions"

    document_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), index=True, nullable=False
    )
    document_type: Mapped[str] = mapped_column(String(50), nullable=False)
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="COMPLETED", index=True, nullable=False)
    error_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    raw_response: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    structured_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string; NULL on failure
    prompt_version: Mapped[str] = mapped_column(String(20), default="v1.0", nullable=False)
    processing_time_ms: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    input_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    output_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    estimated_cost: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # NULL when pricing unknown
    confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # NULL on failure
    confidence_details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON breakdown
    final_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # reviewer-approved data (JSON)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    # Relationship
    document: Mapped["Document"] = relationship("Document", back_populates="ai_extractions")

    def __repr__(self) -> str:
        return f"<AIExtraction(id={self.id}, document_id={self.document_id}, type='{self.document_type}', status='{self.status}')>"
