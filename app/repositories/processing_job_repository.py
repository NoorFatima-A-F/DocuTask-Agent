"""
ProcessingJobRepository Data Persistence Layer.
Implements persistence operations for asynchronous ProcessingJob entities.
"""

import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy import select, func, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document
from app.models.processing_job import ProcessingJob
from app.repositories.base import BaseRepository


class ProcessingJobRepository(BaseRepository[ProcessingJob]):
    """Repository handling persistence operations for ProcessingJob entity."""

    def __init__(self, db: AsyncSession):
        super().__init__(model=ProcessingJob, db=db)

    async def create(self, job_data: Dict[str, Any]) -> ProcessingJob:
        """Creates and persists a new background job record."""
        job = ProcessingJob(**job_data)
        self.db.add(job)
        await self.db.flush()
        await self.db.refresh(job)
        return job

    async def get_by_id(self, job_id: uuid.UUID) -> Optional[ProcessingJob]:
        """Retrieves background job by UUID."""
        result = await self.db.execute(
            select(ProcessingJob).where(ProcessingJob.id == job_id)
        )
        return result.scalar_one_or_none()

    async def get_pending_jobs(self, limit: int = 10) -> List[ProcessingJob]:
        """Retrieves pending QUEUED jobs ordered by priority descending and created_at ascending."""
        query = (
            select(ProcessingJob)
            .where(ProcessingJob.status.in_(["QUEUED", "RETRYING"]))
            .order_by(ProcessingJob.priority.desc(), ProcessingJob.created_at.asc())
            .limit(limit)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_running_jobs(self) -> List[ProcessingJob]:
        """Retrieves currently active RUNNING jobs."""
        query = select(ProcessingJob).where(ProcessingJob.status == "RUNNING")
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_failed_jobs(self, limit: int = 10) -> List[ProcessingJob]:
        """Retrieves failed jobs for inspection."""
        query = select(ProcessingJob).where(ProcessingJob.status == "FAILED").limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_active_job_for_document(self, document_id: uuid.UUID) -> Optional[ProcessingJob]:
        """Retrieves any currently running or pending job for specified document."""
        query = (
            select(ProcessingJob)
            .where(
                ProcessingJob.document_id == document_id,
                ProcessingJob.status.in_(["QUEUED", "RUNNING", "RETRYING"])
            )
            .limit(1)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def list_jobs(
        self,
        owner_id: uuid.UUID,
        skip: int = 0,
        limit: int = 20
    ) -> Tuple[List[ProcessingJob], int]:
        """Retrieves paginated background jobs owned by specified user via document relationship."""
        count_stmt = (
            select(func.count(ProcessingJob.id))
            .join(Document, ProcessingJob.document_id == Document.id)
            .where(Document.owner_id == owner_id)
        )
        count_res = await self.db.execute(count_stmt)
        total = count_res.scalar() or 0

        stmt = (
            select(ProcessingJob)
            .join(Document, ProcessingJob.document_id == Document.id)
            .where(Document.owner_id == owner_id)
            .order_by(ProcessingJob.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all()), total

    async def update_status(
        self,
        job: ProcessingJob,
        status: str,
        progress: float = 0.0,
        last_error: Optional[str] = None
    ) -> ProcessingJob:
        """Updates job status, progress percentage, and timestamps."""
        job.status = status
        job.progress = max(0.0, min(100.0, progress))
        if last_error:
            job.last_error = last_error
        
        now = datetime.now(timezone.utc)
        if status == "RUNNING" and not job.started_at:
            job.started_at = now
        elif status in ("COMPLETED", "FAILED", "CANCELLED"):
            job.completed_at = now

        self.db.add(job)
        await self.db.flush()
        await self.db.refresh(job)
        return job

    async def increment_attempt(self, job: ProcessingJob) -> ProcessingJob:
        """Increments job execution attempt counter."""
        job.attempts += 1
        self.db.add(job)
        await self.db.flush()
        await self.db.refresh(job)
        return job

    async def cancel(self, job: ProcessingJob) -> ProcessingJob:
        """Cancels a job."""
        return await self.update_status(job, status="CANCELLED", progress=job.progress, last_error="Cancelled by user request")

    async def delete(self, job: ProcessingJob) -> None:
        """Deletes job record."""
        await self.db.delete(job)
        await self.db.flush()
