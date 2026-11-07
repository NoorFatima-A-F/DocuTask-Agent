"""Background job request/response schemas."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class JobCreateRequest(BaseModel):
    document_id: UUID
    document_type: str = Field("generic", min_length=1, max_length=50, description="invoice, receipt, resume, ...")


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    document_id: UUID
    document_type: str
    status: str = Field(..., description="QUEUED, RUNNING, RETRYING, COMPLETED, NEEDS_REVIEW or FAILED")
    attempts: int
    max_attempts: int
    error_code: Optional[str] = None
    last_error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class JobListResponse(BaseModel):
    items: List[JobResponse]
    total: int
    page: int
    page_size: int
    pages: int
