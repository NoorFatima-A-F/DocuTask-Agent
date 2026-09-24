"""
Job Dispatcher Module.
Enqueues document processing jobs, checks active job duplicate prevention, and manages job lifecycles.
"""

import math
from uuid import UUID

from app.core.exceptions import ResourceNotFoundException
from app.core.logging import logger
from app.models.user import User
from app.repositories.document_repository import DocumentRepository
from app.repositories.processing_job_repository import ProcessingJobRepository
from app.schemas.job import JobListResponse, ProcessingJobResponse
from app.workers.base import JobQueueProvider
from app.workers.exceptions import DuplicateJobException, JobNotFoundException
from app.workers.jobs import JobTask, JobType, JobState


class JobDispatcher:
    """Dispatcher managing job creation, queuing, and duplicate prevention."""

    def __init__(
        self,
        job_repo: ProcessingJobRepository,
        doc_repo: DocumentRepository,
        queue_provider: JobQueueProvider
    ):
        self.job_repo = job_repo
        self.doc_repo = doc_repo
        self.queue = queue_provider

    async def enqueue_document_pipeline(
        self,
        document_id: UUID,
        owner: User,
        document_type: str = "generic",
        priority: int = 1,
        force_reextract: bool = False
    ) -> ProcessingJobResponse:
        """
        Enqueues an asynchronous document extraction job with duplicate active job protection.
        """
        doc = await self.doc_repo.get_by_id(document_id)
        if not doc or (doc.owner_id != owner.id and not owner.is_superuser):
            raise ResourceNotFoundException("Document not found")

        # Duplicate job prevention: Check if active job already running for this document
        active_job = await self.job_repo.get_active_job_for_document(document_id)
        if active_job and not force_reextract:
            logger.warning(f"Active job '{active_job.id}' already running for document '{document_id}'")
            raise DuplicateJobException(
                f"An active background job '{active_job.id}' is already processing this document."
            )

        # Create ProcessingJob record in database
        job_record = await self.job_repo.create({
            "document_id": document_id,
            "job_type": JobType.DOCUMENT_PIPELINE.value,
            "status": JobState.QUEUED.value,
            "priority": priority,
            "attempts": 0,
            "max_attempts": 3,
            "progress": 0.0,
            "last_error": None
        })

        # Update document status to QUEUED
        await self.doc_repo.update_status(doc, "QUEUED")

        # Enqueue memory task object
        task = JobTask(
            job_id=job_record.id,
            document_id=document_id,
            job_type=JobType.DOCUMENT_PIPELINE.value,
            priority=priority,
            max_attempts=3,
            payload={
                "owner_id": str(owner.id),
                "document_type": document_type,
                "force_reextract": force_reextract
            }
        )
        await self.queue.enqueue(task)

        logger.info(f"Dispatched background job '{job_record.id}' for document '{document_id}'")
        return ProcessingJobResponse.model_validate(job_record)

    async def get_job_status(self, job_id: UUID, owner: User) -> ProcessingJobResponse:
        """Retrieves current job status and progress percentage."""
        job = await self.job_repo.get_by_id(job_id)
        if not job:
            raise JobNotFoundException("Job not found")

        # Verify document ownership
        doc = await self.doc_repo.get_by_id(job.document_id)
        if not doc or (doc.owner_id != owner.id and not owner.is_superuser):
            raise JobNotFoundException("Job not found")

        return ProcessingJobResponse.model_validate(job)

    async def list_user_jobs(
        self,
        owner: User,
        page: int = 1,
        page_size: int = 20
    ) -> JobListResponse:
        """Lists user background jobs with pagination."""
        page = max(1, page)
        page_size = max(1, min(100, page_size))
        skip = (page - 1) * page_size

        jobs, total = await self.job_repo.list_jobs(owner_id=owner.id, skip=skip, limit=page_size)
        pages = math.ceil(total / page_size) if total > 0 else 0

        items = [ProcessingJobResponse.model_validate(j) for j in jobs]
        return JobListResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            pages=pages
        )

    async def cancel_job(self, job_id: UUID, owner: User) -> ProcessingJobResponse:
        """Cancels a queued or running job."""
        job = await self.job_repo.get_by_id(job_id)
        if not job:
            raise JobNotFoundException("Job not found")

        doc = await self.doc_repo.get_by_id(job.document_id)
        if not doc or (doc.owner_id != owner.id and not owner.is_superuser):
            raise JobNotFoundException("Job not found")

        await self.queue.cancel(job_id)
        cancelled_job = await self.job_repo.cancel(job)
        return ProcessingJobResponse.model_validate(cancelled_job)
