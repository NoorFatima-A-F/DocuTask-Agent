"""Celery task wrapping :func:`app.jobs.runner.execute_job`."""

from __future__ import annotations

import asyncio
import random
import uuid

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.ai.providers.gemini import GeminiProvider
from app.core.config import settings
from app.jobs.celery_app import celery_app
from app.jobs.runner import JobDependencies, RetryJob, execute_job
from app.ocr.pipeline import OCRPipeline
from app.ocr.providers.tesseract import TesseractOCRProvider
from app.storage.local import LocalStorageProvider

#: Retries after the first attempt, for transient errors only.
MAX_RETRIES = 3
BACKOFF_BASE_SECONDS = 5.0
BACKOFF_CAP_SECONDS = 120.0


def build_dependencies() -> JobDependencies:
    """Real providers for the worker process. Tests replace this function."""
    return JobDependencies(
        ocr_pipeline=OCRPipeline(ocr_provider=TesseractOCRProvider()),
        llm_provider=GeminiProvider(),
        storage=LocalStorageProvider(),
    )


def retry_delay(retries_so_far: int, retry_after: float | None) -> float:
    """Exponential backoff with jitter, never shorter than the provider's Retry-After."""
    backoff = min(BACKOFF_BASE_SECONDS * 2**retries_so_far, BACKOFF_CAP_SECONDS)
    # Jitter only; not security-sensitive.
    backoff += random.uniform(0, BACKOFF_BASE_SECONDS)  # noqa: S311  # nosec B311
    return float(max(backoff, retry_after or 0.0))


async def _run(job_id: uuid.UUID, final_attempt: bool) -> str | None:
    # asyncio.run gives each task a fresh event loop, so the engine must be task-scoped too.
    engine = create_async_engine(settings.DATABASE_URL)
    try:
        factory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)
        return await execute_job(job_id, factory, build_dependencies(), final_attempt=final_attempt)
    finally:
        await engine.dispose()


@celery_app.task(bind=True, name="docutask.run_extraction", max_retries=MAX_RETRIES)  # type: ignore[untyped-decorator]
def run_extraction(self, job_id: str) -> str | None:  # type: ignore[no-untyped-def]
    """Run one attempt of an extraction job; schedule a retry only for transient failures."""
    final_attempt = self.request.retries >= self.max_retries
    try:
        return asyncio.run(_run(uuid.UUID(job_id), final_attempt))
    except RetryJob as exc:
        raise self.retry(exc=exc, countdown=retry_delay(self.request.retries, exc.retry_after)) from exc
