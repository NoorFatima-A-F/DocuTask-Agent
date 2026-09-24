"""
ProcessingJob SQLAlchemy ORM Model.
Tracks asynchronous background job status, attempts, progress percentages, and worker execution logs.
"""

import uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.document import Document


class ProcessingJob(Base, UUIDMixin, TimestampMixin):
    """ProcessingJob database entity representation."""

    __tablename__ = "processing_jobs"

    document_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("documents.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    job_type: Mapped[str] = mapped_column(String(50), default="DOCUMENT_PIPELINE", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="QUEUED", index=True, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    max_attempts: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    progress: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    worker_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Relationship
    document: Mapped["Document"] = relationship("Document", back_populates="processing_jobs")

    def __repr__(self) -> str:
        return f"<ProcessingJob(id={self.id}, document_id={self.document_id}, status='{self.status}', progress={self.progress}%)>"
