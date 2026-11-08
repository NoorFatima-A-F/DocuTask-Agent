"""Persistence for ProcessingJob rows."""

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document
from app.models.processing_job import JobStatus, ProcessingJob
from app.repositories.base import BaseRepository


class ProcessingJobRepository(BaseRepository[ProcessingJob]):
    """Queries for background jobs."""

    def __init__(self, db: AsyncSession):
        super().__init__(model=ProcessingJob, db=db)

    async def add(self, job: ProcessingJob) -> ProcessingJob:
        self.db.add(job)
        await self.db.flush()
        await self.db.refresh(job)
        return job

    async def get_by_id(self, job_id: uuid.UUID) -> ProcessingJob | None:
        result = await self.db.execute(select(ProcessingJob).where(ProcessingJob.id == job_id))
        return result.scalar_one_or_none()

    async def get_by_idempotency_key(self, key: str) -> ProcessingJob | None:
        result = await self.db.execute(select(ProcessingJob).where(ProcessingJob.idempotency_key == key))
        return result.scalar_one_or_none()

    async def list_for_owner(
        self, owner_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> tuple[list[ProcessingJob], int]:
        """Jobs whose document belongs to ``owner_id``, newest first."""
        owned = (
            select(ProcessingJob)
            .join(Document, ProcessingJob.document_id == Document.id)
            .where(Document.owner_id == owner_id)
        )
        total = (await self.db.execute(select(func.count()).select_from(owned.subquery()))).scalar() or 0
        rows = await self.db.execute(owned.order_by(ProcessingJob.created_at.desc()).offset(skip).limit(limit))
        return list(rows.scalars().all()), total

    async def list_failed(self, skip: int = 0, limit: int = 50) -> tuple[list[ProcessingJob], int]:
        """All FAILED jobs (admin view), newest first."""
        failed = select(ProcessingJob).where(ProcessingJob.status == JobStatus.FAILED.value)
        total = (await self.db.execute(select(func.count()).select_from(failed.subquery()))).scalar() or 0
        rows = await self.db.execute(failed.order_by(ProcessingJob.updated_at.desc()).offset(skip).limit(limit))
        return list(rows.scalars().all()), total
