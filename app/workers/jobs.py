"""
Job States, Types, and Task Representations.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict
from uuid import UUID


class JobState(str, Enum):
    """Possible background job processing states."""
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    RETRYING = "RETRYING"


class JobType(str, Enum):
    """Types of background jobs."""
    DOCUMENT_PIPELINE = "DOCUMENT_PIPELINE"
    OCR_EXTRACTION = "OCR_EXTRACTION"
    AI_EXTRACTION = "AI_EXTRACTION"


@dataclass
class JobTask:
    """Internal memory representation of a background job task."""
    job_id: UUID
    document_id: UUID
    job_type: str = JobType.DOCUMENT_PIPELINE.value
    priority: int = 1
    attempts: int = 0
    max_attempts: int = 3
    payload: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
