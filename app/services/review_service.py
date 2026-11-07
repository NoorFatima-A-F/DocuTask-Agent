"""Human review of low-confidence extractions (the NEEDS_REVIEW queue)."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.exceptions import AIValidationException
from app.ai.validator import AIValidator
from app.core.errors.extraction import ErrorCode, ExtractionStatus
from app.core.exceptions import BaseAppException, ResourceNotFoundException, ValidationAppException
from app.core.logging import logger
from app.core.security import sanitize_log_input
from app.models.ai_extraction import AIExtraction
from app.models.document import Document
from app.models.extracted_text import ExtractedText
from app.models.review_event import ReviewEvent
from app.models.user import User


class ReviewConflictException(BaseAppException):
    """The extraction is not (or no longer) awaiting review."""

    def __init__(self, message: str = "Extraction is not awaiting review"):
        super().__init__(message=message, status_code=409)


class ReviewService:
    """Lists, inspects, approves and rejects extractions awaiting human review."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_pending(self, page: int = 1, page_size: int = 20) -> Tuple[List[AIExtraction], int]:
        page, page_size = max(1, page), max(1, min(100, page_size))
        pending = AIExtraction.status == ExtractionStatus.NEEDS_REVIEW.value
        total = (await self.db.execute(select(func.count()).select_from(AIExtraction).where(pending))).scalar() or 0
        rows = await self.db.execute(
            select(AIExtraction)
            .where(pending)
            .order_by(AIExtraction.created_at.asc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        return list(rows.scalars().all()), int(total)

    async def get(self, extraction_id: UUID) -> AIExtraction:
        record = await self.db.get(AIExtraction, extraction_id)
        if record is None:
            raise ResourceNotFoundException("Extraction not found")
        return record

    async def get_detail(self, extraction_id: UUID) -> Dict[str, Any]:
        record = await self.get(extraction_id)
        doc = await self.db.get(Document, record.document_id)
        pages = await self.db.execute(
            select(ExtractedText)
            .where(ExtractedText.document_id == record.document_id)
            .order_by(ExtractedText.page_number.asc())
        )
        ocr_text = "\n\n".join(p.text for p in pages.scalars().all() if p.text)
        return {"record": record, "document": doc, "ocr_text": ocr_text}

    async def get_document_path(self, extraction_id: UUID) -> Tuple[str, str, str]:
        record = await self.get(extraction_id)
        doc = await self.db.get(Document, record.document_id)
        if doc is None:
            raise ResourceNotFoundException("Document not found")
        return doc.absolute_path, doc.mime_type, doc.original_filename

    async def approve(self, extraction_id: UUID, reviewer: User, corrections: Optional[Dict[str, Any]]) -> AIExtraction:
        record = await self._pending(extraction_id)
        original = json.loads(record.structured_json) if record.structured_json else {}
        if corrections:
            try:
                final = AIValidator.validate({**original, **corrections}, record.document_type)
            except AIValidationException as exc:
                raise ValidationAppException(exc.message, errors=exc.errors) from exc
        else:
            final = original

        record.status = ExtractionStatus.COMPLETED.value
        record.final_json = json.dumps(final)
        self.db.add(
            ReviewEvent(
                extraction_id=record.id,
                reviewer_id=reviewer.id,
                action="APPROVED",
                original_json=record.structured_json,
                corrected_json=json.dumps(corrections) if corrections else None,
            )
        )
        await self._set_document_status(record.document_id, "EXTRACTION_COMPLETED")
        await self.db.flush()
        logger.info(
            "Extraction '%s' approved by reviewer '%s' (corrected=%s)",
            sanitize_log_input(record.id),
            sanitize_log_input(reviewer.id),
            bool(corrections),
        )
        return record

    async def reject(self, extraction_id: UUID, reviewer: User, reason: str) -> AIExtraction:
        record = await self._pending(extraction_id)
        record.status = ExtractionStatus.FAILED.value
        record.error_code = ErrorCode.REJECTED_BY_REVIEWER.value
        record.error_message = "Rejected by reviewer."
        record.final_json = None
        self.db.add(
            ReviewEvent(
                extraction_id=record.id,
                reviewer_id=reviewer.id,
                action="REJECTED",
                original_json=record.structured_json,
                reason=reason,
            )
        )
        await self._set_document_status(record.document_id, "EXTRACTION_FAILED")
        await self.db.flush()
        logger.info(
            "Extraction '%s' rejected by reviewer '%s'", sanitize_log_input(record.id), sanitize_log_input(reviewer.id)
        )
        return record

    async def events_for(self, extraction_id: UUID) -> List[ReviewEvent]:
        rows = await self.db.execute(
            select(ReviewEvent).where(ReviewEvent.extraction_id == extraction_id).order_by(ReviewEvent.created_at)
        )
        return list(rows.scalars().all())

    async def _pending(self, extraction_id: UUID) -> AIExtraction:
        record = await self.get(extraction_id)
        if record.status != ExtractionStatus.NEEDS_REVIEW.value:
            raise ReviewConflictException()
        return record

    async def _set_document_status(self, document_id: UUID, status: str) -> None:
        doc = await self.db.get(Document, document_id)
        if doc is not None:
            doc.upload_status = status
