"""Background job request/response schemas."""

from datetime import datetime
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
    error_code: str | None = None
    last_error: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class JobListResponse(BaseModel):
    items: list[JobResponse]
    total: int
    page: int
    page_size: int
    pages: int
