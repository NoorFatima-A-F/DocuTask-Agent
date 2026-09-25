"""
ExtractedText SQLAlchemy ORM Model.
Stores page-level extracted text, confidence metrics, and extraction methodology.
"""

import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, UUIDMixin

if TYPE_CHECKING:
    from app.models.document import Document


class ExtractedText(Base, UUIDMixin):
    """ExtractedText database entity representation."""

    __tablename__ = "extracted_texts"

    document_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("documents.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    page_number: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    processing_method: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationship
    document: Mapped["Document"] = relationship("Document", back_populates="extracted_pages")

    def __repr__(self) -> str:
        return f"<ExtractedText(id={self.id}, document_id={self.document_id}, page={self.page_number}, method='{self.processing_method}')>"
