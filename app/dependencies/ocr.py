"""
OCR Provider & Pipeline Dependency Injector.
"""

from app.ocr.base import OCRProvider
from app.ocr.pipeline import OCRPipeline
from app.ocr.providers.tesseract import TesseractOCRProvider

_ocr_provider_instance: OCRProvider = TesseractOCRProvider()
_ocr_pipeline_instance: OCRPipeline = OCRPipeline(ocr_provider=_ocr_provider_instance)


def get_ocr_provider() -> OCRProvider:
    """Provides active OCRProvider instance."""
    return _ocr_provider_instance


def get_ocr_pipeline() -> OCRPipeline:
    """Provides active OCRPipeline instance."""
    return _ocr_pipeline_instance
