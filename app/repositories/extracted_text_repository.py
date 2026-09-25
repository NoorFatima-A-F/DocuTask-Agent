"""
ExtractedTextRepository Data Persistence Layer.
Implements persistence and retrieval for page-level extracted document text.
"""

import uuid
from typing import Dict, Any, List
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.extracted_text import ExtractedText
from app.repositories.base import BaseRepository


class ExtractedTextRepository(BaseRepository[ExtractedText]):
    """Repository handling persistence operations for ExtractedText entity."""

    def __init__(self, db: AsyncSession):
        super().__init__(model=ExtractedText, db=db)

    async def create(self, extracted_data: Dict[str, Any]) -> ExtractedText:
        """Creates and persists a single page extracted text record."""
        record = ExtractedText(**extracted_data)
        self.db.add(record)
        await self.db.flush()
        await self.db.refresh(record)
        return record

    async def bulk_create(self, pages_data: List[Dict[str, Any]]) -> List[ExtractedText]:
        """Bulk persists multiple page extracted text records."""
        records = [ExtractedText(**data) for data in pages_data]
        self.db.add_all(records)
        await self.db.flush()
        for r in records:
            await self.db.refresh(r)
        return records

    async def get_document_text(self, document_id: uuid.UUID) -> List[ExtractedText]:
        """Retrieves all extracted text pages for document ordered by page_number."""
        query = (
            select(ExtractedText)
            .where(ExtractedText.document_id == document_id)
            .order_by(ExtractedText.page_number.asc())
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def delete_document_text(self, document_id: uuid.UUID) -> None:
        """Deletes all extracted text records for a given document."""
        await self.db.execute(
            delete(ExtractedText).where(ExtractedText.document_id == document_id)
        )
        await self.db.flush()
