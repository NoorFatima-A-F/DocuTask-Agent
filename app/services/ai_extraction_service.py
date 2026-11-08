"""
AI structured extraction service.

Orchestrates OCR text -> LLM -> schema validation -> persistence. Fail-closed: every
failure is persisted as a FAILED extraction record (no structured data, no confidence),
the document is marked EXTRACTION_FAILED, and the typed error is re-raised.
"""

import asyncio
import json
import random
import time
from collections.abc import Awaitable, Callable
from typing import Any
from uuid import UUID

from app.ai.base import LLMProvider, LLMResult
from app.ai.confidence import assess, routing_status
from app.ai.exceptions import AIValidationException
from app.ai.prompt_builder import PromptBuilder
from app.ai.schemas import (
    ExtractionMetadata,
    ExtractionRequest,
    ExtractionResponse,
    ExtractionResult,
    ExtractionStatistics,
)
from app.ai.validator import AIValidator
from app.core.config import settings
from app.core.errors.extraction import ErrorCode, ExtractionError, ExtractionStatus, LLMError, OCRError
from app.core.exceptions import ResourceNotFoundException, ValidationAppException
from app.core.logging import logger
from app.core.security import sanitize_log_input
from app.models.ai_extraction import AIExtraction
from app.models.document import Document
from app.models.user import User
from app.repositories.ai_extraction_repository import AIExtractionRepository
from app.repositories.document_repository import DocumentRepository
from app.services.ocr_service import OCRService

PROMPT_VERSION = "v1.0"
INTERNAL_ERROR_CODE = "INTERNAL_ERROR"
DOCUMENT_STATUS_BY_RESULT = {
    ExtractionStatus.COMPLETED: "EXTRACTION_COMPLETED",
    ExtractionStatus.NEEDS_REVIEW: "EXTRACTION_NEEDS_REVIEW",
}


class AIExtractionService:
    """Service handling AI structured document extraction workflow."""

    #: Total attempts for transient provider errors (429, 5xx, timeout).
    MAX_TRANSIENT_ATTEMPTS = 3
    #: Extra attempts with a corrective prompt when output fails schema validation.
    MAX_SCHEMA_RETRIES = 2
    BACKOFF_BASE_SECONDS = 1.0
    BACKOFF_CAP_SECONDS = 30.0

    def __init__(
        self,
        document_repo: DocumentRepository,
        ai_extraction_repo: AIExtractionRepository,
        ocr_service: OCRService,
        llm_provider: LLMProvider,
        sleep: Callable[[float], Awaitable[Any]] = asyncio.sleep,
        max_transient_attempts: int | None = None,
    ):
        #: Background jobs pass 1 so the job queue owns retries (durable, honours Retry-After).
        self.max_transient_attempts = max_transient_attempts or self.MAX_TRANSIENT_ATTEMPTS
        self.doc_repo = document_repo
        self.ai_repo = ai_extraction_repo
        self.ocr_service = ocr_service
        self.llm = llm_provider
        self._sleep = sleep

    @staticmethod
    def _to_response_schema(record: AIExtraction, retry_count: int = 0) -> ExtractionResponse:
        """Converts database ORM entity to ExtractionResponse Pydantic schema."""
        parsed_json = json.loads(record.structured_json) if record.structured_json else None
        final_json = json.loads(record.final_json) if record.final_json else None
        details = json.loads(record.confidence_details) if record.confidence_details else None
        return ExtractionResponse(
            id=record.id,
            metadata=ExtractionMetadata(
                document_id=record.document_id,
                document_type=record.document_type,
                provider=record.provider,
                model=record.model,
                prompt_version=record.prompt_version,
                created_at=record.created_at,
            ),
            statistics=ExtractionStatistics(
                processing_time_ms=record.processing_time_ms,
                input_tokens=record.input_tokens,
                output_tokens=record.output_tokens,
                estimated_cost=record.estimated_cost,
                retry_count=retry_count,
            ),
            result=ExtractionResult(
                status=record.status,
                raw_response=record.raw_response,
                structured_json=parsed_json,
                final_json=final_json,
                confidence=record.confidence,
                confidence_details=details,
                error_code=record.error_code,
                error_message=record.error_message,
            ),
        )

    async def _get_owned_document(self, document_id: UUID, owner: User) -> Document:
        doc = await self.doc_repo.get_by_id(document_id)
        if not doc or (doc.owner_id != owner.id and not owner.is_superuser):
            if doc:
                logger.warning(
                    "Unauthorized AI extraction access: User '%s' on Document '%s'",
                    sanitize_log_input(owner.id),
                    sanitize_log_input(document_id),
                )
            raise ResourceNotFoundException("Document not found")
        return doc

    async def _call_llm(
        self, prompt: str, json_schema: dict[str, Any], system_instruction: str, model: str
    ) -> LLMResult:
        """Call the provider, retrying only transient errors with exponential backoff + jitter."""
        attempt = 1
        while True:
            try:
                return await self.llm.generate_json(
                    prompt=prompt, json_schema=json_schema, system_instruction=system_instruction, model=model
                )
            except LLMError as exc:
                if not exc.transient or attempt >= self.max_transient_attempts:
                    raise
                if exc.retry_after is not None:
                    delay = min(exc.retry_after, self.BACKOFF_CAP_SECONDS)
                else:
                    delay = min(self.BACKOFF_BASE_SECONDS * 2 ** (attempt - 1), self.BACKOFF_CAP_SECONDS)
                delay += random.uniform(0, self.BACKOFF_BASE_SECONDS)  # noqa: S311  # nosec B311
                logger.warning(
                    "Transient LLM error %s (attempt %d/%d); retrying in %.1fs",
                    exc.error_code,
                    attempt,
                    self.max_transient_attempts,
                    delay,
                )
                await self._sleep(delay)
                attempt += 1

    async def extract_structured_data(
        self, document_id: UUID, owner: User, request: ExtractionRequest
    ) -> ExtractionResponse:
        """Run OCR (if needed), call the LLM, validate, and persist the extraction."""
        doc = await self._get_owned_document(document_id, owner)
        doc_type = request.document_type.lower().strip()

        if request.provider and request.provider.lower().strip() != self.llm.provider_name:
            raise ValidationAppException(f"Unsupported LLM provider '{request.provider}'")

        if not request.force_reextract:
            cached = await self.ai_repo.get_latest(document_id, document_type=doc_type, exclude_failed=True)
            if cached:
                logger.info(
                    "Returning cached AI extraction for document '%s' type '%s'",
                    sanitize_log_input(document_id),
                    sanitize_log_input(doc_type),
                )
                return self._to_response_schema(cached)

        target_model = request.model or self.llm.default_model
        await self.doc_repo.update_status(doc, "EXTRACTION_RUNNING")

        start_time = time.perf_counter()
        usage = {"input": 0, "output": 0}
        try:
            return await self._run_extraction(doc, owner, doc_type, target_model, start_time, usage)
        except Exception as exc:
            await self._record_failure(doc, doc_type, target_model, exc, start_time, usage)
            raise

    async def _run_extraction(
        self,
        doc: Document,
        owner: User,
        doc_type: str,
        target_model: str,
        start_time: float,
        usage: dict[str, int],
    ) -> ExtractionResponse:
        try:
            doc_content = await self.ocr_service.get_extracted_text(doc.id, owner)
        except ResourceNotFoundException:
            doc_content = await self.ocr_service.extract_text_for_document(doc.id, owner)
        if not doc_content.text or not doc_content.text.strip():
            raise OCRError(ErrorCode.OCR_NO_TEXT)

        boundary = PromptBuilder.new_boundary()
        system_instruction = PromptBuilder.build_system_instruction(doc_type, boundary)
        user_prompt = PromptBuilder.build_prompt(doc_content.text, doc_type, boundary)
        json_schema = PromptBuilder.get_json_schema(doc_type)

        current_prompt = user_prompt
        validated: dict[str, Any] | None = None
        raw_response = ""
        retry_count = 0
        for attempt in range(self.MAX_SCHEMA_RETRIES + 1):
            try:
                result = await self._call_llm(current_prompt, json_schema, system_instruction, target_model)
                usage["input"] += result.input_tokens
                usage["output"] += result.output_tokens
                raw_response = result.raw_text
                validated = AIValidator.validate(result.data, doc_type)
                break
            except (AIValidationException, LLMError) as exc:
                if isinstance(exc, LLMError) and exc.code != ErrorCode.LLM_INVALID_OUTPUT:
                    raise
                if attempt == self.MAX_SCHEMA_RETRIES:
                    raise LLMError(
                        ErrorCode.LLM_INVALID_OUTPUT,
                        f"LLM output failed schema validation after {attempt + 1} attempts.",
                    ) from exc
                retry_count += 1
                logger.warning(
                    "LLM output invalid for doc '%s' (attempt %d); retrying with corrective prompt",
                    sanitize_log_input(doc.id),
                    attempt + 1,
                )
                current_prompt = (
                    f"{user_prompt}\n\n"
                    "CORRECTION REQUIRED: your previous response was not valid for the required schema "
                    f"({exc.message}). Respond again with a single JSON object that conforms to the schema."
                )

        if validated is None:  # unreachable: the loop either breaks with a value or raises
            raise LLMError(ErrorCode.LLM_INVALID_OUTPUT)
        threshold = settings.CONFIDENCE_THRESHOLD_HITL
        report = assess(doc_type, validated, doc_content.text, doc_content.average_confidence, threshold)
        status = routing_status(report, threshold)

        processing_time_ms = int((time.perf_counter() - start_time) * 1000)
        record = await self.ai_repo.create(
            {
                "document_id": doc.id,
                "document_type": doc_type,
                "provider": self.llm.provider_name,
                "model": target_model,
                "status": status.value,
                "raw_response": raw_response,
                "structured_json": json.dumps(validated),
                # Only auto-accepted results become final; NEEDS_REVIEW waits for a reviewer.
                "final_json": json.dumps(validated) if status == ExtractionStatus.COMPLETED else None,
                "prompt_version": PROMPT_VERSION,
                "processing_time_ms": processing_time_ms,
                "input_tokens": usage["input"],
                "output_tokens": usage["output"],
                "estimated_cost": self.llm.calculate_cost(usage["input"], usage["output"], target_model),
                "confidence": report.score,
                "confidence_details": json.dumps(report.to_dict(), default=str),
            }
        )
        await self.doc_repo.update_status(doc, DOCUMENT_STATUS_BY_RESULT[status])
        logger.info(
            "AI extraction finished for doc '%s': type=%s status=%s confidence=%.3f time=%dms",
            sanitize_log_input(doc.id),
            sanitize_log_input(doc_type),
            status.value,
            report.score,
            processing_time_ms,
        )
        return self._to_response_schema(record, retry_count=retry_count)

    async def _record_failure(
        self,
        doc: Document,
        doc_type: str,
        model: str,
        exc: Exception,
        start_time: float,
        usage: dict[str, int],
    ) -> None:
        """Persist a FAILED extraction row and EXTRACTION_FAILED document status, then commit.

        The commit is explicit because the request-scoped session rolls back when the
        error propagates; without it the failure record would be lost.
        """
        if isinstance(exc, ExtractionError):
            error_code, error_message = exc.error_code, exc.message
        else:
            error_code, error_message = INTERNAL_ERROR_CODE, "Unexpected internal error during extraction."
        document_id = doc.id
        logger.error(
            "AI extraction failed for document '%s': %s (%s)",
            sanitize_log_input(document_id),
            error_code,
            type(exc).__name__,
        )
        try:
            await self.ai_repo.create(
                {
                    "document_id": document_id,
                    "document_type": doc_type,
                    "provider": self.llm.provider_name,
                    "model": model,
                    "status": ExtractionStatus.FAILED.value,
                    "error_code": error_code,
                    "error_message": error_message,
                    "raw_response": None,
                    "structured_json": None,
                    "confidence": None,
                    "prompt_version": PROMPT_VERSION,
                    "processing_time_ms": int((time.perf_counter() - start_time) * 1000),
                    "input_tokens": usage["input"],
                    "output_tokens": usage["output"],
                    "estimated_cost": None,
                }
            )
            await self.doc_repo.update_status(doc, "EXTRACTION_FAILED")
            await self.ai_repo.db.commit()
        except Exception as persist_exc:
            logger.error("Could not persist extraction failure record: %s", type(persist_exc).__name__)

    async def get_latest_result(self, document_id: UUID, owner: User) -> ExtractionResponse:
        """Most recent extraction for a document, whatever its status (clients must check ``status``)."""
        await self._get_owned_document(document_id, owner)
        latest = await self.ai_repo.get_latest(document_id)
        if not latest:
            raise ResourceNotFoundException("No AI extraction results found for this document. Run extraction first.")
        return self._to_response_schema(latest)

    async def get_extraction_status(self, document_id: UUID, owner: User) -> dict[str, Any]:
        """Retrieves AI extraction operational status for a document."""
        doc = await self._get_owned_document(document_id, owner)
        latest = await self.ai_repo.get_latest(document_id)
        return {
            "document_id": document_id,
            "status": doc.upload_status,
            "has_extraction": latest is not None,
            "extraction_status": latest.status if latest else None,
            "error_code": latest.error_code if latest else None,
            "document_type": latest.document_type if latest else None,
            "confidence": latest.confidence if latest else None,
        }

    async def get_extraction_history(self, document_id: UUID, owner: User) -> list[ExtractionResponse]:
        """Retrieves complete history of past AI extractions for a document."""
        await self._get_owned_document(document_id, owner)
        records = await self.ai_repo.get_history(document_id)
        return [self._to_response_schema(r) for r in records]

    async def delete_result(self, document_id: UUID, owner: User) -> None:
        """Deletes the latest AI extraction result for a document."""
        await self._get_owned_document(document_id, owner)
        latest = await self.ai_repo.get_latest(document_id)
        if latest:
            await self.ai_repo.delete(latest.id)
            logger.info("Deleted AI extraction result for document '%s'", sanitize_log_input(document_id))
