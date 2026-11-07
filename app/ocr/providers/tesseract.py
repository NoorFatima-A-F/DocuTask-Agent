"""Tesseract OCR provider (pytesseract + Pillow).

Failures are typed: a missing ``tesseract`` binary raises ``OCR_ENGINE_UNAVAILABLE``,
any other engine failure raises ``OCR_FAILED``, and undecodable input raises
``CorruptedDocumentException``. Confidence is the mean of Tesseract's word-level
confidences from ``image_to_data``; when no word confidences exist it is ``None``.
"""

from __future__ import annotations

import io
import shutil

import pytesseract
from PIL import Image

from app.core.errors.extraction import ErrorCode, OCRError
from app.core.logging import logger
from app.ocr.base import OCRProvider
from app.ocr.exceptions import CorruptedDocumentException
from app.ocr.preprocessor import ImagePreprocessor
from app.ocr.schemas import PageContent


class TesseractOCRProvider(OCRProvider):
    """Concrete OCRProvider using the Tesseract OCR engine."""

    SUPPORTED_EXTENSIONS = frozenset({".png", ".jpg", ".jpeg", ".tiff", ".tif", ".bmp", ".webp"})
    SUPPORTED_MIMES = frozenset({"image/png", "image/jpeg", "image/tiff", "image/bmp", "image/webp"})

    @property
    def provider_name(self) -> str:
        return "tesseract"

    def supports(self, file_extension_or_mime: str) -> bool:
        val = file_extension_or_mime.lower().strip()
        return val in self.SUPPORTED_EXTENSIONS or val in self.SUPPORTED_MIMES

    def is_available(self) -> bool:
        cmd = pytesseract.pytesseract.tesseract_cmd
        return shutil.which(cmd) is not None

    @staticmethod
    def _open_image(image_bytes: bytes) -> Image.Image:
        if not image_bytes:
            raise CorruptedDocumentException("Image byte stream is empty")
        try:
            Image.open(io.BytesIO(image_bytes)).verify()
            image = Image.open(io.BytesIO(image_bytes))
            return ImagePreprocessor.preprocess_image(image)
        except Exception as exc:
            logger.warning("Failed to decode image content: %s", type(exc).__name__)
            raise CorruptedDocumentException("Corrupted or unreadable image file") from exc

    async def extract_page(self, image_bytes: bytes, page_number: int = 1, language: str = "eng") -> PageContent:
        image = self._open_image(image_bytes)
        try:
            text = pytesseract.image_to_string(image, lang=language).strip()
            data = pytesseract.image_to_data(image, lang=language, output_type=pytesseract.Output.DICT)
        except pytesseract.TesseractNotFoundError as exc:
            raise OCRError(ErrorCode.OCR_ENGINE_UNAVAILABLE) from exc
        except (pytesseract.TesseractError, RuntimeError, OSError) as exc:
            logger.warning("Tesseract failed on page %d: %s", page_number, type(exc).__name__)
            raise OCRError(ErrorCode.OCR_FAILED) from exc

        return PageContent(
            page_number=page_number,
            text=text,
            confidence=word_confidence(data),
            processing_method="ocr",
        )


def word_confidence(data: dict) -> float | None:  # type: ignore[type-arg]
    """Mean word confidence (0..1) from ``image_to_data`` output, or ``None`` if there are no words."""
    confs: list[float] = []
    for raw_conf, word in zip(data.get("conf", []), data.get("text", []), strict=False):
        try:
            conf = float(raw_conf)
        except (TypeError, ValueError):
            continue
        if conf >= 0 and str(word).strip():
            confs.append(conf)
    if not confs:
        return None
    return round(sum(confs) / len(confs) / 100.0, 4)
