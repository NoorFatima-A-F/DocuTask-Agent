"""
Abstract OCR Provider Plugin Interface.
Defines base class for swappable OCR engines (Tesseract, Document AI, Textract, Azure, PaddleOCR).
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseOCRProvider(ABC):
    """Abstract base class for all OCR engine implementations."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Returns unique identifier name for the OCR provider."""
        pass

    @abstractmethod
    async def extract_text(self, document_bytes: bytes, filename: str) -> Dict[str, Any]:
        """
        Processes document bytes and returns extracted text & metadata payload.
        """
        pass


# Alias for backward compatibility across pipeline
OCRProvider = BaseOCRProvider

