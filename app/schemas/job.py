"""
ProcessingJob Request and Response Pydantic Schemas.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class JobStatusEnum(str, Enum):
    """Job processing lifecycle states."""
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    RETRYING = "RETRYING"


class JobTypeEnum(str, Enum):
    """Types of asynchronous jobs."""
    DOCUMENT_PIPELINE = "DOCUMENT_PIPELINE"
    OCR_EXTRACTION = "OCR_EXTRACTION"
    AI_EXTRACTION = "AI_EXTRACTION"


class EnqueueJobRequest(BaseModel):
    """Payload to queue an asynchronous document extraction job."""

    document_type: str = Field("generic", description="Target document schema type (invoice, resume, etc.)")
    priority: int = Field(1, ge=1, le=10, description="Job priority (1=Normal, 10=High)")
    force_reextract: bool = Field(False, description="Bypass cache and force re-processing")


class ProcessingJobResponse(BaseModel):
    """Response payload for background processing job."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    document_id: UUID
    job_type: str
    status: str
    priority: int
    attempts: int
    max_attempts: int
    progress: float = Field(..., description="Progress percentage (0.0 to 100.0)")
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    last_error: Optional[str] = None
    worker_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class JobListResponse(BaseModel):
    """Paginated background job list response."""

    items: List[ProcessingJobResponse]
    total: int
    page: int
    page_size: int
    pages: int
