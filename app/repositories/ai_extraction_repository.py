"""
AIExtractionRepository Data Persistence Layer.
Implements metadata and structured JSON persistence for LLM extractions.
"""

import uuid
from typing import Any

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ai_extraction import AIExtraction
from app.repositories.base import BaseRepository


class AIExtractionRepository(BaseRepository[AIExtraction]):
    """Repository handling persistence operations for AIExtraction entity."""

    def __init__(self, db: AsyncSession):
        super().__init__(model=AIExtraction, db=db)

    async def create(self, extraction_data: dict[str, Any]) -> AIExtraction:
        """Creates and persists a new AI extraction record."""
        record = AIExtraction(**extraction_data)
        self.db.add(record)
        await self.db.flush()
        await self.db.refresh(record)
        return record

    async def get_latest(
        self, document_id: uuid.UUID, document_type: str | None = None, exclude_failed: bool = False
    ) -> AIExtraction | None:
        """Most recent extraction record for a document (optionally ignoring FAILED rows)."""
        query = select(AIExtraction).where(AIExtraction.document_id == document_id)
        if document_type:
            query = query.where(AIExtraction.document_type == document_type)
        if exclude_failed:
            query = query.where(AIExtraction.status != "FAILED")
        query = query.order_by(AIExtraction.created_at.desc()).limit(1)

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_history(self, document_id: uuid.UUID) -> list[AIExtraction]:
        """Retrieves all past extraction history records for document."""
        query = (
            select(AIExtraction).where(AIExtraction.document_id == document_id).order_by(AIExtraction.created_at.desc())
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def delete(self, extraction_id: uuid.UUID) -> None:
        """Deletes extraction record from persistence."""
        await self.db.execute(delete(AIExtraction).where(AIExtraction.id == extraction_id))
        await self.db.flush()
