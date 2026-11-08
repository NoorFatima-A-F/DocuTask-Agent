"""Submit, inspect and retry background extraction jobs."""

from __future__ import annotations

import hashlib
import math
import uuid
from typing import Callable, Optional

from fastapi.concurrency import run_in_threadpool
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.errors.extraction import ErrorCode, ExtractionError
from app.core.exceptions import BaseAppException, ResourceNotFoundException
from app.core.logging import logger
from app.models.processing_job import JobStatus, ProcessingJob
from app.models.user import User
from app.repositories.document_repository import DocumentRepository
from app.repositories.processing_job_repository import ProcessingJobRepository
from app.schemas.job import JobListResponse, JobResponse

#: Publishes a job id to the queue. Raises if the broker is unreachable.
Enqueuer = Callable[[uuid.UUID], None]


class JobConflictException(BaseAppException):
    def __init__(self, message: str):
        super().__init__(message=message, status_code=409)


def celery_enqueuer(job_id: uuid.UUID) -> None:
    """Publish to Redis via Celery. Refuses (fails closed) when no broker is configured."""
    if not settings.REDIS_URL:
        raise ExtractionError(ErrorCode.QUEUE_UNAVAILABLE, "REDIS_URL is not configured; cannot queue jobs.")
    from app.jobs.tasks import run_extraction  # noqa: PLC0415 - keep celery out of API import time

    run_extraction.apply_async(args=[str(job_id)], retry=False)


def idempotency_key(owner_id: uuid.UUID, document_id: uuid.UUID, document_type: str, client_key: str | None) -> str:
    """Scope keys per user. Without a client key, one job per (document, type)."""
    raw = f"{owner_id}:client:{client_key}" if client_key else f"{owner_id}:{document_id}:{document_type}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


class JobService:
    def __init__(self, db: AsyncSession, enqueue: Enqueuer):
        self.db = db
        self.jobs = ProcessingJobRepository(db)
        self.docs = DocumentRepository(db)
        self.enqueue = enqueue

    async def submit(
        self, owner: User, document_id: uuid.UUID, document_type: str, client_key: Optional[str] = None
    ) -> tuple[JobResponse, bool]:
        """Create and enqueue a job; returns ``(job, created)``. Resubmissions return the existing job."""
        doc = await self.docs.get_by_id(document_id)
        if doc is None or (doc.owner_id != owner.id and not owner.is_superuser):
            raise ResourceNotFoundException("Document not found")

        document_type = document_type.lower().strip()
        key = idempotency_key(owner.id, document_id, document_type, client_key)
        existing = await self.jobs.get_by_idempotency_key(key)
        if existing is None:
            from app.jobs.tasks import MAX_RETRIES  # noqa: PLC0415

            job = ProcessingJob(
                document_id=document_id,
                document_type=document_type,
                idempotency_key=key,
                status=JobStatus.QUEUED.value,
                attempts=0,
                max_attempts=MAX_RETRIES + 1,
            )
            try:
                await self.jobs.add(job)
                await self.db.commit()
            except IntegrityError:  # a concurrent identical submission won the race
                await self.db.rollback()
                existing = await self.jobs.get_by_idempotency_key(key)
                if existing is None:
                    raise
        if existing is not None:
            if existing.document_id != document_id or existing.document_type != document_type:
                raise JobConflictException("Idempotency-Key was already used for a different request")
            return JobResponse.model_validate(existing), False

        await self._enqueue(job)
        return JobResponse.model_validate(job), True

    async def get(self, owner: User, job_id: uuid.UUID) -> JobResponse:
        return JobResponse.model_validate(await self._owned(owner, job_id))

    async def list_for_owner(self, owner: User, page: int, page_size: int) -> JobListResponse:
        items, total = await self.jobs.list_for_owner(owner.id, skip=(page - 1) * page_size, limit=page_size)
        return self._page(items, total, page, page_size)

    async def list_failed(self, page: int, page_size: int) -> JobListResponse:
        items, total = await self.jobs.list_failed(skip=(page - 1) * page_size, limit=page_size)
        return self._page(items, total, page, page_size)

    async def retry(self, owner: User, job_id: uuid.UUID) -> JobResponse:
        """Re-queue a FAILED job as a fresh run (attempt counter reset)."""
        job = await self._owned(owner, job_id)
        if job.status != JobStatus.FAILED.value:
            raise JobConflictException(f"Only FAILED jobs can be retried (job is {job.status})")
        job.status = JobStatus.QUEUED.value
        job.attempts = 0
        job.error_code = None
        job.last_error = None
        job.completed_at = None
        await self.db.commit()
        await self._enqueue(job)
        return JobResponse.model_validate(job)

    async def _enqueue(self, job: ProcessingJob) -> None:
        try:
            await run_in_threadpool(self.enqueue, job.id)
        except Exception as exc:
            code = exc.code if isinstance(exc, ExtractionError) else ErrorCode.QUEUE_UNAVAILABLE
            logger.error("Could not enqueue job %s: %s", job.id, type(exc).__name__)
            job.status = JobStatus.FAILED.value
            job.error_code = code.value
            job.last_error = exc.message if isinstance(exc, ExtractionError) else "Job queue is not reachable"
            await self.db.commit()
            raise ExtractionError(code, job.last_error) from exc
        logger.info("Queued job %s for document %s", job.id, job.document_id)

    async def _owned(self, owner: User, job_id: uuid.UUID) -> ProcessingJob:
        job = await self.jobs.get_by_id(job_id)
        doc = await self.docs.get_by_id(job.document_id) if job else None
        if job is None or doc is None or (doc.owner_id != owner.id and not owner.is_superuser):
            raise ResourceNotFoundException("Job not found")
        return job

    @staticmethod
    def _page(items: list[ProcessingJob], total: int, page: int, page_size: int) -> JobListResponse:
        return JobListResponse(
            items=[JobResponse.model_validate(j) for j in items],
            total=total,
            page=page,
            page_size=page_size,
            pages=math.ceil(total / page_size) if total else 0,
        )
