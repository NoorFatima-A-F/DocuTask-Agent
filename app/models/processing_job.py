"""ProcessingJob: one background extraction run (OCR -> LLM -> validation) for a document."""

import uuid
from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.document import Document


class JobStatus(StrEnum):
    """Lifecycle of a background job. COMPLETED/NEEDS_REVIEW mirror the extraction routing."""

    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    RETRYING = "RETRYING"
    COMPLETED = "COMPLETED"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    FAILED = "FAILED"


#: A redelivered task for a job in one of these states is a no-op.
FINISHED_JOB_STATUSES = frozenset({JobStatus.COMPLETED.value, JobStatus.NEEDS_REVIEW.value, JobStatus.FAILED.value})


class ProcessingJob(Base, UUIDMixin, TimestampMixin):
    """A queued/running/finished extraction job. The row, not the broker, is the source of truth."""

    __tablename__ = "processing_jobs"

    document_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), index=True, nullable=False
    )
    document_type: Mapped[str] = mapped_column(String(50), default="generic", nullable=False)
    #: sha256 of (owner, client Idempotency-Key or document+type); unique so a resubmission returns the same job.
    idempotency_key: Mapped[str | None] = mapped_column(String(64), unique=True, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default=JobStatus.QUEUED.value, index=True, nullable=False)
    attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    max_attempts: Mapped[int] = mapped_column(Integer, default=4, nullable=False)
    error_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    document: Mapped["Document"] = relationship("Document", back_populates="processing_jobs")

    def __repr__(self) -> str:
        return f"<ProcessingJob(id={self.id}, document_id={self.document_id}, status='{self.status}')>"
