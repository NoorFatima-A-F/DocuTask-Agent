"""
Validation Subsystem SQLAlchemy ORM Models.
Stores validation evaluation runs, document results, and benchmark metrics in database with performance indexes.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, UUIDMixin


class ValidationRun(Base, UUIDMixin):
    """ValidationRun database entity for tracking evaluation benchmark runs."""

    __tablename__ = "validation_runs"

    version_tag: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    model_name: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    total_documents: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    average_accuracy: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    average_f1_score: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    regression_status: Mapped[str] = mapped_column(String(20), nullable=False, default="NONE")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True,
        nullable=False
    )

    # Relationships
    results: Mapped[list["ValidationResult"]] = relationship("ValidationResult", back_populates="run", cascade="all, delete-orphan")


class ValidationResult(Base, UUIDMixin):
    """ValidationResult entity storing per-document evaluation scores."""

    __tablename__ = "validation_results"

    run_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("validation_runs.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    document_id: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    document_type: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    field_accuracy: Mapped[float] = mapped_column(Float, nullable=False)
    f1_score: Mapped[float] = mapped_column(Float, nullable=False)
    evidence_path: Mapped[str] = mapped_column(Text, nullable=False)
    pass_fail: Mapped[str] = mapped_column(String(10), nullable=False, default="PASS")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True,
        nullable=False
    )

    # Relationship
    run: Mapped["ValidationRun"] = relationship("ValidationRun", back_populates="results")
