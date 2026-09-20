"""
Document SQLAlchemy ORM Model.
Stores document metadata, file system path references, and processing status.
"""

import uuid
from typing import TYPE_CHECKING
from sqlalchemy import BigInteger, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.extracted_text import ExtractedText
    from app.models.ai_extraction import AIExtraction
    from app.models.processing_job import ProcessingJob


class Document(Base, UUIDMixin, TimestampMixin):
    """Document database entity representation."""

    __tablename__ = "documents"

    owner_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    stored_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    relative_path: Mapped[str] = mapped_column(String(512), nullable=False)
    absolute_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    file_extension: Mapped[str] = mapped_column(String(20), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    file_size: Mapped[int] = mapped_column(BigInteger, nullable=False)
    sha256_hash: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    upload_status: Mapped[str] = mapped_column(String(50), default="QUEUED", nullable=False)

    # Relationships
    owner: Mapped["User"] = relationship("User", back_populates="documents")
    extracted_pages: Mapped[List["ExtractedText"]] = relationship(
        "ExtractedText",
        back_populates="document",
        cascade="all, delete-orphan",
        order_by="ExtractedText.page_number",
        lazy="selectin"
    )
    ai_extractions: Mapped[List["AIExtraction"]] = relationship(
        "AIExtraction",
        back_populates="document",
        cascade="all, delete-orphan",
        order_by="AIExtraction.created_at.desc()",
        lazy="selectin"
    )
    processing_jobs: Mapped[List["ProcessingJob"]] = relationship(
        "ProcessingJob",
        back_populates="document",
        cascade="all, delete-orphan",
        order_by="ProcessingJob.created_at.desc()",
        lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Document(id={self.id}, original_filename='{self.original_filename}', status='{self.upload_status}')>"
