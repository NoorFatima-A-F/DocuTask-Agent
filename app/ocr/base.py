"""OCR provider contract.

A provider extracts one page of text from an image, or raises
:class:`app.core.errors.extraction.OCRError` / ``CorruptedDocumentException``.
It never returns placeholder text or a guessed confidence.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.ocr.schemas import PageContent


class OCRProvider(ABC):
    """Abstract base class for OCR engines."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Unique identifier, e.g. ``tesseract``."""

    @abstractmethod
    async def extract_page(self, image_bytes: bytes, page_number: int = 1, language: str = "eng") -> PageContent:
        """OCR a single page image."""

    def is_available(self) -> bool:
        """Whether the engine can run in this environment (used by readiness)."""
        return True
