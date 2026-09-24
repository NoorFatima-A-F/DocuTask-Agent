"""
Async Worker Engine Module.
Polls job queue, claims tasks, executes OCR and AI extraction pipelines, updates progress,
and enforces exponential backoff retry strategies.
"""

import asyncio
import uuid
from typing import Optional

from app.ai.schemas import ExtractionRequest

from app.core.logging import logger
from app.database.session import AsyncSessionLocal
from app.repositories.ai_extraction_repository import AIExtractionRepository
from app.repositories.document_repository import DocumentRepository
from app.repositories.extracted_text_repository import ExtractedTextRepository
from app.repositories.processing_job_repository import ProcessingJobRepository
from app.repositories.user_repository import UserRepository
from app.services.ai_extraction_service import AIExtractionService
from app.services.ocr_service import OCRService
from app.storage.local import LocalStorageProvider
from app.ocr.pipeline import OCRPipeline
from app.ocr.providers.tesseract import TesseractOCRProvider
from app.workers.base import JobQueueProvider
from app.workers.jobs import JobState, JobTask


class AsyncWorkerEngine:
    """Background worker engine consuming job tasks from queue."""

    def __init__(self, queue_provider: JobQueueProvider, worker_name: str = "AsyncWorker-1"):
        self.queue = queue_provider
        self.worker_name = worker_name
        self._running = False
        self._loop_task: Optional[asyncio.Task] = None

    async def start(self) -> None:
        """Starts worker polling background loop."""
        if not self._running:
            self._running = True
            self._loop_task = asyncio.create_task(self._worker_loop())
            logger.info(f"Worker Engine [{self.worker_name}] started successfully.")

    async def stop(self) -> None:
        """Stops worker polling loop gracefully."""
        if self._running:
            self._running = False
            if self._loop_task:
                self._loop_task.cancel()
                try:
                    await self._loop_task
                except asyncio.CancelledError:
                    pass
            logger.info(f"Worker Engine [{self.worker_name}] stopped.")

    async def _worker_loop(self) -> None:
        """Worker main polling loop."""
        while self._running:
            try:
                task = await self.queue.dequeue(timeout=1.0)
                if task:
                    await self._execute_task(task)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Worker Engine error in loop: {str(e)}", exc_info=True)
                await asyncio.sleep(1.0)

    async def _execute_task(self, task: JobTask) -> None:
        """Executes a single job task within isolated database session."""
        logger.info(f"Worker [{self.worker_name}] processing job '{task.job_id}' (Doc='{task.document_id}')")

        async with AsyncSessionLocal() as db:
            job_repo = ProcessingJobRepository(db)
            doc_repo = DocumentRepository(db)
            text_repo = ExtractedTextRepository(db)
            ai_repo = AIExtractionRepository(db)
            user_repo = UserRepository(db)
            storage = LocalStorageProvider()

            ocr_service = OCRService(
                document_repo=doc_repo,
                extracted_text_repo=text_repo,
                storage_provider=storage,
                ocr_pipeline=OCRPipeline(ocr_provider=TesseractOCRProvider())
            )
            ai_service = AIExtractionService(
                document_repo=doc_repo,
                ai_extraction_repo=ai_repo,
                ocr_service=ocr_service
            )

            job = await job_repo.get_by_id(task.job_id)
            if not job:
                logger.warning(f"Job record '{task.job_id}' not found in database.")
                return

            if job.status == JobState.CANCELLED.value:
                logger.info(f"Job '{task.job_id}' was cancelled. Skipping execution.")
                return

            # Increment attempt counter
            await job_repo.increment_attempt(job)
            await job_repo.update_status(job, status=JobState.RUNNING.value, progress=10.0)
            job.worker_name = self.worker_name

            payload = task.payload or {}
            owner_id_str = payload.get("owner_id")
            doc_type = payload.get("document_type", "generic")
            force = payload.get("force_reextract", False)

            owner = await user_repo.get_by_id(uuid.UUID(owner_id_str)) if owner_id_str else None
            if not owner:
                doc = await doc_repo.get_by_id(task.document_id)
                owner = doc.owner if doc else None

            if not owner:
                err_msg = f"Owner user record for document '{task.document_id}' not found"
                await job_repo.update_status(job, status=JobState.FAILED.value, progress=0.0, last_error=err_msg)
                return

            try:
                # Step 1: OCR Text Extraction (Progress 40%)
                logger.info(f"Job '{task.job_id}': Running OCR text extraction...")
                await ocr_service.extract_text_for_document(task.document_id, owner, force_reextract=force)
                await job_repo.update_status(job, status=JobState.RUNNING.value, progress=40.0)

                # Step 2: AI Structured Extraction (Progress 80%)
                logger.info(f"Job '{task.job_id}': Running AI structured extraction for type '{doc_type}'...")
                req = ExtractionRequest(document_type=doc_type, force_reextract=force)
                await ai_service.extract_structured_data(task.document_id, owner, req)
                await job_repo.update_status(job, status=JobState.RUNNING.value, progress=80.0)

                # Step 3: Complete Job (Progress 100%)
                await job_repo.update_status(job, status=JobState.COMPLETED.value, progress=100.0)
                await db.commit()
                logger.info(f"Job '{task.job_id}' successfully COMPLETED.")

            except Exception as exc:
                await db.rollback()
                err_msg = str(exc)
                logger.error(f"Job '{task.job_id}' execution failed: {err_msg}")

                # Retry Policy with Exponential Backoff
                if job.attempts < job.max_attempts:
                    backoff_delay = 2 * (2 ** (job.attempts - 1))  # 2s, 4s, 8s
                    logger.info(f"Scheduling retry {job.attempts}/{job.max_attempts} for job '{task.job_id}' in {backoff_delay}s")
                    await job_repo.update_status(
                        job,
                        status=JobState.RETRYING.value,
                        progress=0.0,
                        last_error=f"Attempt {job.attempts} failed: {err_msg}"
                    )
                    await db.commit()

                    # Re-enqueue after backoff
                    await asyncio.sleep(backoff_delay)
                    await self.queue.enqueue(task)
                else:
                    logger.error(f"Job '{task.job_id}' exhausted max attempts ({job.max_attempts}). Marking FAILED.")
                    await job_repo.update_status(
                        job,
                        status=JobState.FAILED.value,
                        progress=0.0,
                        last_error=f"Exhausted max retries ({job.max_attempts}): {err_msg}"
                    )
                    doc = await doc_repo.get_by_id(task.document_id)
                    if doc:
                        await doc_repo.update_status(doc, "FAILED")
                    await db.commit()
