"""Scripted OCR provider for tests. Lives in tests/ only; never imported by app/."""

from __future__ import annotations

from app.ocr.base import OCRProvider
from app.ocr.schemas import PageContent


class FakeOCRProvider(OCRProvider):
    """Returns fixed text for every page, or raises a scripted exception."""

    def __init__(self, text: str = "", confidence: float | None = 0.95, error: BaseException | None = None):
        self.text = text
        self.confidence = confidence
        self.error = error
        self.calls = 0

    @property
    def provider_name(self) -> str:
        return "fake-ocr"

    async def extract_page(self, image_bytes: bytes, page_number: int = 1, language: str = "eng") -> PageContent:
        self.calls += 1
        if self.error is not None:
            raise self.error
        return PageContent(page_number=page_number, text=self.text, confidence=self.confidence, processing_method="ocr")
