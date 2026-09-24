"""
OCR Service Business Logic Layer.
Coordinates document text extraction, result caching, page persistence, status tracking, and authorization.
"""

from typing import Any, Dict, List
from uuid import UUID

from app.core.exceptions import ResourceNotFoundException
from app.core.logging import logger
from app.core.security import sanitize_log_input
from app.models.user import User
from app.ocr.pipeline import OCRPipeline
from app.ocr.schemas import DocumentContent, PageContent
from app.repositories.document_repository import DocumentRepository
from app.repositories.extracted_text_repository import ExtractedTextRepository
from app.storage.base import StorageProvider


class OCRService:
    """Service providing document text extraction orchestration and persistence."""

    def __init__(
        self,
        document_repo: DocumentRepository,
        extracted_text_repo: ExtractedTextRepository,
        storage_provider: StorageProvider,
        ocr_pipeline: OCRPipeline
    ):
        self.doc_repo = document_repo
        self.text_repo = extracted_text_repo
        self.storage = storage_provider
        self.pipeline = ocr_pipeline

    async def extract_text_for_document(
        self,
        document_id: UUID,
        owner: User,
        force_reextract: bool = False,
        language: str = "eng"
    ) -> DocumentContent:
        """
        Extracts text from document. Utilizes caching unless force_reextract is True.
        Persists page-level results to database within transactional boundary.
        """
        doc = await self.doc_repo.get_by_id(document_id)
        if not doc:
            raise ResourceNotFoundException("Document not found")

        # Multi-tenant isolation check
        if doc.owner_id != owner.id and not owner.is_superuser:
            logger.warning(f"Unauthorized OCR extraction attempt: User '{sanitize_log_input(owner.id)}' on Document '{sanitize_log_input(document_id)}'")
            raise ResourceNotFoundException("Document not found")

        # Caching check
        if not force_reextract:
            existing_pages = await self.text_repo.get_document_text(document_id)
            if existing_pages:
                logger.info(f"Returning cached extracted text for document '{sanitize_log_input(document_id)}'")
                page_contents = [
                    PageContent(
                        page_number=p.page_number,
                        text=p.text,
                        confidence=p.confidence,
                        processing_method=p.processing_method
                    ) for p in existing_pages
                ]
                total_conf = sum(p.confidence for p in page_contents)
                avg_conf = round(total_conf / len(page_contents), 4)
                full_text = "\n\n".join([p.text for p in page_contents if p.text.strip()])

                return DocumentContent(
                    document_id=document_id,
                    page_count=len(page_contents),
                    text=full_text,
                    pages=page_contents,
                    average_confidence=avg_conf
                )

        # Update status to OCR_RUNNING
        await self.doc_repo.update_status(doc, "OCR_RUNNING")

        try:
            # Read document binary content from storage
            file_bytes = await self.storage.read(doc.relative_path)

            # Execute OCR pipeline
            doc_content = await self.pipeline.process(
                document_id=document_id,
                file_content=file_bytes,
                file_extension=doc.file_extension,
                mime_type=doc.mime_type,
                language=language
            )

            # Clear existing records if re-extracting
            if force_reextract:
                await self.text_repo.delete_document_text(document_id)

            # Persist extracted page results
            pages_to_create = [
                {
                    "document_id": document_id,
                    "page_number": page.page_number,
                    "text": page.text,
                    "confidence": page.confidence,
                    "processing_method": page.processing_method
                } for page in doc_content.pages
            ]
            await self.text_repo.bulk_create(pages_to_create)

            # Update status to OCR_COMPLETED
            await self.doc_repo.update_status(doc, "OCR_COMPLETED")

            logger.info(f"Persisted text extraction for document '{sanitize_log_input(document_id)}': {len(pages_to_create)} pages")
            return doc_content

        except Exception as exc:
            logger.error(f"OCR text extraction failed for document '{sanitize_log_input(document_id)}': {sanitize_log_input(exc)}")
            await self.doc_repo.update_status(doc, "OCR_FAILED")
            raise exc

    async def get_extracted_text(self, document_id: UUID, owner: User) -> DocumentContent:
        """Retrieves previously extracted text for a document from database."""
        doc = await self.doc_repo.get_by_id(document_id)
        if not doc:
            raise ResourceNotFoundException("Document not found")

        if doc.owner_id != owner.id and not owner.is_superuser:
            raise ResourceNotFoundException("Document not found")

        extracted_pages = await self.text_repo.get_document_text(document_id)
        if not extracted_pages:
            raise ResourceNotFoundException("No extracted text found for this document. Please trigger extraction first.")

        page_contents = [
            PageContent(
                page_number=p.page_number,
                text=p.text,
                confidence=p.confidence,
                processing_method=p.processing_method
            ) for p in extracted_pages
        ]
        total_conf = sum(p.confidence for p in page_contents)
        avg_conf = round(total_conf / len(page_contents), 4)
        full_text = "\n\n".join([p.text for p in page_contents if p.text.strip()])

        return DocumentContent(
            document_id=document_id,
            page_count=len(page_contents),
            text=full_text,
            pages=page_contents,
            average_confidence=avg_conf
        )

    async def get_extracted_pages(self, document_id: UUID, owner: User) -> List[PageContent]:
        """Retrieves page breakdown of extracted text for a document."""
        doc_content = await self.get_extracted_text(document_id, owner)
        return doc_content.pages

    async def get_ocr_status(self, document_id: UUID, owner: User) -> Dict[str, Any]:
        """Retrieves current OCR extraction status and metrics for a document."""
        doc = await self.doc_repo.get_by_id(document_id)
        if not doc:
            raise ResourceNotFoundException("Document not found")

        if doc.owner_id != owner.id and not owner.is_superuser:
            raise ResourceNotFoundException("Document not found")

        extracted_pages = await self.text_repo.get_document_text(document_id)
        page_count = len(extracted_pages)
        avg_conf = (
            round(sum(p.confidence for p in extracted_pages) / page_count, 4)
            if page_count > 0
            else 0.0
        )

        return {
            "document_id": document_id,
            "status": doc.upload_status,
            "page_count": page_count,
            "average_confidence": avg_conf,
            "has_extracted_text": page_count > 0
        }
