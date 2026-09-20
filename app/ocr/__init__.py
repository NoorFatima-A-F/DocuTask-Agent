"""
OCR & Text Extraction Package.
Provides document classification, native text extraction, and OCR engine integration.
"""

from app.ocr.base import OCRProvider
from app.ocr.pipeline import OCRPipeline
from app.ocr.schemas import DocumentContent, PageContent

__all__ = ["OCRProvider", "OCRPipeline", "DocumentContent", "PageContent"]
