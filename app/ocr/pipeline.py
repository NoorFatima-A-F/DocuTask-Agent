"""
OCR Pipeline Orchestrator.
Coordinates document detection, digital PDF / text native extraction, OCR execution, and output aggregation.
"""

from collections.abc import Sequence
from uuid import UUID

from app.core.errors.extraction import ErrorCode, OCRError
from app.core.logging import logger
from app.core.security import sanitize_log_input
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
        self, document_id: UUID, file_content: bytes, file_extension: str, mime_type: str, language: str = "eng"
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
        logger.info("OCR Pipeline selected strategy [%s] for document '%s'", doc_type, sanitize_log_input(document_id))

        pages: list[PageContent] = []

        if doc_type == "txt":
            # Native TXT decoding (100% confidence)
            try:
                decoded_text = file_content.decode("utf-8")
            except UnicodeDecodeError:
                decoded_text = file_content.decode("latin-1", errors="ignore")
            pages.append(
                PageContent(page_number=1, text=decoded_text.strip(), confidence=1.0, processing_method="native_txt")
            )

        elif doc_type == "image":
            # Image OCR
            page = await self.ocr_provider.extract_page(file_content, page_number=1, language=language)
            pages.append(page)

        elif doc_type in ("native_pdf", "scanned_pdf"):
            # PDF Processing (Native selectable text or per-page OCR fallback)
            pages = await self.pdf_processor.process_pdf(file_content)

        else:
            logger.error(
                "Unsupported document format encountered: ext='%s', mime='%s'",
                sanitize_log_input(file_extension),
                sanitize_log_input(mime_type),
            )
            raise UnsupportedFileTypeException(f"Unsupported document format '{file_extension}'")

        merged_text = merge_page_text(pages)
        if not merged_text:
            raise OCRError(ErrorCode.OCR_NO_TEXT)
        avg_confidence = average_confidence(pages)

        logger.info(
            "Extraction completed for doc '%s': Strategy=%s, Pages=%d, AvgConfidence=%s",
            sanitize_log_input(document_id),
            doc_type,
            len(pages),
            avg_confidence,
        )

        return DocumentContent(
            document_id=document_id,
            page_count=len(pages),
            text=merged_text,
            pages=pages,
            average_confidence=avg_confidence,
        )


def merge_page_text(pages: Sequence[PageContent]) -> str:
    """Join non-empty page texts with blank lines."""
    return "\n\n".join(p.text.strip() for p in pages if p.text and p.text.strip())


def average_confidence(pages: Sequence[PageContent]) -> float | None:
    """Mean confidence over pages that reported one; ``None`` when no page did."""
    confs = [p.confidence for p in pages if p.confidence is not None]
    return round(sum(confs) / len(confs), 4) if confs else None
