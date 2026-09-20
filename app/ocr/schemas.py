"""
OCR & Extraction Output Schemas.
Defines standardized page-level and document-level extracted text data objects.
"""

from typing import List
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class PageContent(BaseModel):
    """Extracted text payload for a single document page."""

    model_config = ConfigDict(from_attributes=True)

    page_number: int = Field(..., description="1-based page index")
    text: str = Field(..., description="Extracted plain text content")
    confidence: float = Field(..., description="Extraction confidence score (0.0 to 1.0)")
    processing_method: str = Field(..., description="'native_pdf' or 'ocr'")


class DocumentContent(BaseModel):
    """Standardized aggregated extracted text output for a document."""

    model_config = ConfigDict(from_attributes=True)

    document_id: UUID = Field(..., description="ID of extracted document")
    page_count: int = Field(..., description="Total pages processed")
    text: str = Field(..., description="Aggregated full document text")
    pages: List[PageContent] = Field(default_factory=list, description="Per-page extracted text breakdown")
    average_confidence: float = Field(..., description="Average confidence score across all pages (0.0 to 1.0)")
