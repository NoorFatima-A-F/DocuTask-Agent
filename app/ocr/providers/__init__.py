"""OCR provider implementations."""

from app.ocr.providers.pdf import PDFProcessor
from app.ocr.providers.tesseract import TesseractOCRProvider

__all__ = ["PDFProcessor", "TesseractOCRProvider"]
