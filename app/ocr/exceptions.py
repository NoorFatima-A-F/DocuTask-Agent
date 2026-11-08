"""
OCR & Extraction Domain Exceptions.
"""

from typing import Any

from app.core.exceptions import BaseAppException


class OCRException(BaseAppException):
    """Base exception for OCR engine processing failures."""

    def __init__(self, message: str = "OCR processing failed", errors: Any = None) -> None:
        super().__init__(message=message, status_code=500, errors=errors)


class CorruptedDocumentException(BaseAppException):
    """Raised when uploaded file is corrupted or unreadable by OCR engine."""

    def __init__(self, message: str = "Document is corrupted or unreadable", errors: Any = None) -> None:
        super().__init__(message=message, status_code=422, errors=errors)


class UnsupportedFileTypeException(BaseAppException):
    """Raised when document format is unsupported by OCR extraction pipeline."""

    def __init__(self, message: str = "Unsupported document format for text extraction", errors: Any = None) -> None:
        super().__init__(message=message, status_code=415, errors=errors)
