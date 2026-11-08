"""Execute one extraction job: OCR -> LLM -> validation, recording the outcome on the job row.

This is the async core of the Celery task. It takes its collaborators as arguments so tests
can run it against an in-memory database with fake OCR/LLM providers.

Outcomes:

* extraction COMPLETED / NEEDS_REVIEW -> job status mirrors it;
* transient failure (rate limit, unavailable, timeout) and attempts left -> job RETRYING,
  then :class:`RetryJob` is raised so the queue schedules another attempt;
* any other failure, or the last attempt -> job FAILED with ``error_code`` and ``last_error``.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.ai.base import LLMProvider
from app.ai.schemas import ExtractionRequest
from app.core.errors.extraction import ErrorCode, ExtractionError
from app.core.logging import logger
from app.models.processing_job import FINISHED_JOB_STATUSES, JobStatus, ProcessingJob
from app.ocr.pipeline import OCRPipeline
from app.repositories.ai_extraction_repository import AIExtractionRepository
from app.repositories.document_repository import DocumentRepository
from app.repositories.extracted_text_repository import ExtractedTextRepository
from app.repositories.processing_job_repository import ProcessingJobRepository
from app.repositories.user_repository import UserRepository
from app.services.ai_extraction_service import AIExtractionService
from app.services.ocr_service import OCRService
from app.storage.base import StorageProvider


@dataclass(frozen=True)
class JobDependencies:
    ocr_pipeline: OCRPipeline
    llm_provider: LLMProvider
    storage: StorageProvider


class RetryJob(Exception):
    """Raised after a transient failure was recorded; the queue should retry the job."""

    def __init__(self, error_code: str, retry_after: float | None = None):
        super().__init__(error_code)
        self.error_code = error_code
        self.retry_after = retry_after


def _finish(job: ProcessingJob, status: JobStatus, error_code: str | None = None, error: str | None = None) -> None:
    job.status = status.value
    job.error_code = error_code
    job.last_error = error
    if status != JobStatus.RETRYING:
        job.completed_at = datetime.now(UTC)


async def execute_job(
    job_id: uuid.UUID,
    session_factory: async_sessionmaker[AsyncSession],
    deps: JobDependencies,
    *,
    final_attempt: bool,
) -> str | None:
    """Run the job and return its final status (``None`` if the job row does not exist)."""
    async with session_factory() as db:
        jobs = ProcessingJobRepository(db)
        job = await jobs.get_by_id(job_id)
        if job is None:
            logger.error("Job %s not found; dropping task", job_id)
            return None
        if job.status in FINISHED_JOB_STATUSES:
            logger.info("Job %s already %s; ignoring redelivery", job_id, job.status)
            return job.status

        job.attempts += 1
        job.status = JobStatus.RUNNING.value
        job.started_at = job.started_at or datetime.now(UTC)
        job.error_code = None
        await db.commit()

        doc_repo = DocumentRepository(db)
        ocr = OCRService(
            document_repo=doc_repo,
            extracted_text_repo=ExtractedTextRepository(db),
            storage_provider=deps.storage,
            ocr_pipeline=deps.ocr_pipeline,
        )
        # One LLM attempt per job attempt: retries are scheduled by the queue, not slept in-process.
        ai = AIExtractionService(
            document_repo=doc_repo,
            ai_extraction_repo=AIExtractionRepository(db),
            ocr_service=ocr,
            llm_provider=deps.llm_provider,
            max_transient_attempts=1,
        )

        try:
            doc = await doc_repo.get_by_id(job.document_id)
            owner = await UserRepository(db).get_by_id(doc.owner_id) if doc else None
            if doc is None or owner is None:
                raise LookupError(f"document {job.document_id} or its owner no longer exists")
            await ocr.extract_text_for_document(job.document_id, owner)
            result = await ai.extract_structured_data(
                job.document_id, owner, ExtractionRequest(document_type=job.document_type)
            )
        except ExtractionError as exc:
            await db.rollback()
            job = await jobs.get_by_id(job_id)
            if job is None:  # deleted while running
                return None
            retry = exc.transient and not final_attempt and job.attempts < job.max_attempts
            _finish(job, JobStatus.RETRYING if retry else JobStatus.FAILED, exc.error_code, exc.message)
            await db.commit()
            logger.warning("Job %s attempt %d failed with %s (%s)", job_id, job.attempts, exc.error_code, job.status)
            if retry:
                raise RetryJob(exc.error_code, exc.retry_after) from exc
            return job.status
        except Exception as exc:
            await db.rollback()
            logger.exception("Job %s failed with an unexpected error", job_id)
            job = await jobs.get_by_id(job_id)
            if job is None:
                return None
            _finish(job, JobStatus.FAILED, ErrorCode.JOB_INTERNAL_ERROR.value, f"{type(exc).__name__}: {exc}")
            await db.commit()
            return job.status

        status = JobStatus(result.result.status)
        _finish(job, status)
        await db.commit()
        logger.info("Job %s finished: %s", job_id, status.value)
        return status.value
