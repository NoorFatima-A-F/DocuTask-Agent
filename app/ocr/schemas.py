"""
OCR & Extraction Output Schemas.
Defines standardized page-level and document-level extracted text data objects.
"""

from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class PageContent(BaseModel):
    """Extracted text payload for a single document page."""

    model_config = ConfigDict(from_attributes=True)

    page_number: int = Field(..., description="1-based page index")
    text: str = Field(..., description="Extracted plain text content")
    confidence: Optional[float] = Field(
        ..., description="Mean OCR word confidence (0.0 to 1.0); null when the engine reported none"
    )
    processing_method: str = Field(..., description="'native_pdf', 'native_txt' or 'ocr'")


class DocumentContent(BaseModel):
    """Standardized aggregated extracted text output for a document."""

    model_config = ConfigDict(from_attributes=True)

    document_id: UUID = Field(..., description="ID of extracted document")
    page_count: int = Field(..., description="Total pages processed")
    text: str = Field(..., description="Aggregated full document text")
    pages: List[PageContent] = Field(default_factory=list, description="Per-page extracted text breakdown")
    average_confidence: Optional[float] = Field(
        ..., description="Mean page confidence over pages that reported one; null if none did"
    )
