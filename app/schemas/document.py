"""
Document Request and Response Pydantic Schemas.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Generic, TypeVar
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class UploadStatusEnum(str, Enum):
    """Possible document processing states."""
    UPLOADING = "UPLOADING"
    QUEUED = "QUEUED"
    OCR_RUNNING = "OCR_RUNNING"
    AI_PROCESSING = "AI_PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class DocumentResponse(BaseModel):
    """Document entity response model."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    owner_id: UUID
    original_filename: str
    stored_filename: str
    relative_path: str
    file_extension: str
    mime_type: str
    file_size: int
    sha256_hash: str
    upload_status: str
    created_at: datetime
    updated_at: datetime


class UploadResponse(BaseModel):
    """Payload returned upon successful document upload or duplicate detection."""

    document: DocumentResponse
    is_duplicate: bool = Field(..., description="True if document was previously uploaded")
    message: str = Field(..., description="Upload status message")


class PaginationRequest(BaseModel):
    """Pagination query parameters."""

    page: int = Field(1, ge=1, description="Page number starting from 1")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")


class SearchRequest(PaginationRequest):
    """Search query request payload."""

    query: Optional[str] = Field(None, description="Filename or metadata search query")


class DocumentListResponse(BaseModel):
    """Paginated document list response."""

    items: List[DocumentResponse]
    total: int = Field(..., description="Total records count")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Page size limit")
    pages: int = Field(..., description="Total pages count")


class DeleteResponse(BaseModel):
    """Payload returned upon document deletion."""

    id: UUID
    message: str = "Document deleted successfully"
