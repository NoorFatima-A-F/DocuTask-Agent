"""
PDF Processing Engine.
Opens PDF files via pdfplumber, detects selectable text vs scanned pages,
extracts native text directly when available, and falls back to OCR per page.
"""

import io
from typing import List
import pdfplumber

from app.core.logging import logger
from app.ocr.base import OCRProvider
from app.ocr.exceptions import CorruptedDocumentException
from app.ocr.schemas import PageContent


class PDFProcessor:
    """Processor handling PDF text extraction and OCR page fallback."""

    def __init__(self, ocr_provider: OCRProvider):
        self.ocr_provider = ocr_provider

    async def process_pdf(self, pdf_bytes: bytes) -> List[PageContent]:
        """
        Processes PDF binary content page by page.
        
        :param pdf_bytes: Binary PDF content
        :return: List of PageContent objects
        :raises CorruptedDocumentException: If PDF byte stream is corrupted
        """
        if not pdf_bytes or len(pdf_bytes) == 0:
            raise CorruptedDocumentException("PDF byte stream is empty")

        pages_content: List[PageContent] = []

        try:
            with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                if not pdf.pages:
                    raise CorruptedDocumentException("PDF contains no pages")

                for page_idx, page in enumerate(pdf.pages, start=1):
                    # Attempt native text extraction
                    native_text = page.extract_text()
                    
                    if native_text and len(native_text.strip()) > 10:
                        logger.info(f"PDF Page {page_idx}: Selectable native text detected ({len(native_text)} chars)")
                        pages_content.append(
                            PageContent(
                                page_number=page_idx,
                                text=native_text.strip(),
                                confidence=1.0,
                                processing_method="native_pdf"
                            )
                        )
                    else:
                        logger.info(f"PDF Page {page_idx}: No selectable text found. Falling back to OCR.")
                        # Render page to image for OCR processing
                        img = page.to_image(resolution=150).original
                        img_byte_arr = io.BytesIO()
                        img.save(img_byte_arr, format="PNG")
                        image_bytes = img_byte_arr.getvalue()

                        page_content = await self.ocr_provider.extract_page(image_bytes, page_number=page_idx)
                        pages_content.append(page_content)

            return pages_content

        except CorruptedDocumentException:
            raise
        except Exception as e:
            logger.error(f"Failed to parse PDF document: {str(e)}")
            raise CorruptedDocumentException(f"Corrupted or unreadable PDF document: {str(e)}")
