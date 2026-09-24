from app.core.security import sanitize_log_input
"""
OCR Pipeline Orchestrator.
Coordinates document detection, digital PDF / text native extraction, OCR execution, and output aggregation.
"""

from typing import List
from uuid import UUID

from app.core.logging import logger
from app.ocr.base import OCRProvider
from app.ocr.detector import DocumentTypeDetector
from app.ocr.exceptions import UnsupportedFileTypeException
from app.ocr.providers.pdf import PDFProcessor
from app.ocr.schemas import DocumentContent, PageContent


class OCRPipeline:
    """Pipeline orchestrating text extraction across document formats."""

    def __init__(self, ocr_provider: OCRProvider):
        self.ocr_provider = ocr_provider
        self.pdf_processor = PDFProcessor(ocr_provider=ocr_provider)

    async def process(
        self,
        document_id: UUID,
        file_content: bytes,
        file_extension: str,
        mime_type: str,
        language: str = "eng"
    ) -> DocumentContent:
        """
        Executes text extraction pipeline on document content.
        
        :param document_id: Unique document identifier
        :param file_content: Binary file content
        :param file_extension: File extension (e.g. '.pdf')
        :param mime_type: File MIME type
        :param language: OCR language code
        :return: DocumentContent object
        """
        doc_type = DocumentTypeDetector.detect_type(file_content, file_extension, mime_type)
        logger.info(f"OCR Pipeline selected strategy [{doc_type}] for document '{sanitize_log_input(document_id)}'")

        pages: List[PageContent] = []

        if doc_type == "txt":
            # Native TXT decoding (100% confidence)
            try:
                decoded_text = file_content.decode("utf-8")
            except UnicodeDecodeError:
                decoded_text = file_content.decode("latin-1", errors="ignore")
            pages.append(
                PageContent(
                    page_number=1,
                    text=decoded_text.strip(),
                    confidence=1.0,
                    processing_method="native_txt"
                )
            )

        elif doc_type == "image":
            # Image OCR
            page = await self.ocr_provider.extract_page(file_content, page_number=1, language=language)
            pages.append(page)

        elif doc_type in ("native_pdf", "scanned_pdf"):
            # PDF Processing (Native selectable text or per-page OCR fallback)
            pages = await self.pdf_processor.process_pdf(file_content)

        else:
            logger.error(f"Unsupported document format encountered: ext='{file_extension}', mime='{mime_type}'")
            raise UnsupportedFileTypeException(f"Unsupported document format '{file_extension}'")

        if not pages:
            pages = [PageContent(page_number=1, text="", confidence=0.0, processing_method="ocr")]

        # Calculate average confidence
        total_conf = sum(p.confidence for p in pages)
        avg_confidence = round(total_conf / len(pages), 4)

        # Merge full document text
        full_text_chunks = [p.text for p in pages if p.text.strip()]
        merged_text = "\n\n".join(full_text_chunks)

        logger.info(
            f"Extraction completed for doc '{sanitize_log_input(document_id)}': Strategy={doc_type}, Pages={len(pages)}, AvgConfidence={avg_confidence}"
        )

        return DocumentContent(
            document_id=document_id,
            page_count=len(pages),
            text=merged_text,
            pages=pages,
            average_confidence=avg_confidence
        )
