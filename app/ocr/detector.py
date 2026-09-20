"""
Document Type Detection Engine.
Classifies input documents into native_pdf, scanned_pdf, image, txt, docx, or unsupported formats.
"""

import io
from typing import Set
import pdfplumber
from PIL import Image

from app.core.logging import logger


class DocumentTypeDetector:
    """Detector for document type classification and OCR necessity determination."""

    IMAGE_EXTENSIONS: Set[str] = {".png", ".jpg", ".jpeg", ".tiff", ".tif", ".bmp", ".webp"}
    IMAGE_MIMES: Set[str] = {
        "image/png", "image/jpeg", "image/tiff", "image/bmp", "image/webp"
    }

    @classmethod
    def detect_type(cls, file_content: bytes, file_extension: str, mime_type: str) -> str:
        """
        Detects document classification strategy.
        
        :return: 'txt', 'docx', 'native_pdf', 'scanned_pdf', 'image', or 'unsupported'
        """
        ext = file_extension.lower().strip()
        mime = mime_type.lower().strip()

        # 1. Plain Text Check
        if ext == ".txt" or mime == "text/plain":
            return "txt"

        # 2. DOCX Check
        if ext == ".docx" or "wordprocessingml" in mime:
            return "docx"

        # 3. Image Check
        if ext in cls.IMAGE_EXTENSIONS or mime in cls.IMAGE_MIMES:
            return "image"

        # 4. PDF Check (inspect for selectable text)
        if ext == ".pdf" or mime == "application/pdf":
            try:
                with pdfplumber.open(io.BytesIO(file_content)) as pdf:
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text and len(text.strip()) > 10:
                            return "native_pdf"
                    return "scanned_pdf"
            except Exception as e:
                logger.warning(f"PDF structure inspection error: {str(e)}")
                return "scanned_pdf"

        return "unsupported"
