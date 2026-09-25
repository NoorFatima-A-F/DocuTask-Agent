"""
DocumentRepository Data Persistence Layer.
Implements metadata persistence, pagination, and search queries for Document entity.
"""

import uuid
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document
from app.repositories.base import BaseRepository


class DocumentRepository(BaseRepository[Document]):
    """Repository handling persistence operations for Document entity."""

    def __init__(self, db: AsyncSession):
        super().__init__(model=Document, db=db)

    async def create(self, doc_data: Dict[str, Any]) -> Document:
        """Creates and persists a new document record."""
        doc = Document(**doc_data)
        self.db.add(doc)
        await self.db.flush()
        await self.db.refresh(doc)
        return doc

    async def get_by_id(self, doc_id: uuid.UUID, owner_id: Optional[uuid.UUID] = None) -> Optional[Document]:
        """Retrieves document by UUID with optional owner isolation check."""
        query = select(Document).where(Document.id == doc_id)
        if owner_id:
            query = query.where(Document.owner_id == owner_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_hash(self, sha256_hash: str, owner_id: Optional[uuid.UUID] = None) -> Optional[Document]:
        """Retrieves document by matching SHA256 hash."""
        query = select(Document).where(Document.sha256_hash == sha256_hash)
        if owner_id:
            query = query.where(Document.owner_id == owner_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def list_documents(self, owner_id: uuid.UUID, skip: int = 0, limit: int = 20) -> List[Document]:
        """Lists documents owned by user ordered by creation timestamp descending."""
        query = (
            select(Document)
            .where(Document.owner_id == owner_id)
            .order_by(Document.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def count_documents(self, owner_id: uuid.UUID, search_term: Optional[str] = None) -> int:
        """Counts total documents owned by user matching optional search term."""
        query = select(func.count(Document.id)).where(Document.owner_id == owner_id)
        if search_term and search_term.strip():
            term = f"%{search_term.strip().lower()}%"
            query = query.where(
                or_(
                    func.lower(Document.original_filename).like(term),
                    func.lower(Document.file_extension).like(term),
                    func.lower(Document.mime_type).like(term)
                )
            )
        result = await self.db.execute(query)
        return result.scalar() or 0

    async def search(self, owner_id: uuid.UUID, query: str, skip: int = 0, limit: int = 20) -> List[Document]:
        """Searches documents by original_filename, file_extension, or mime_type."""
        term = f"%{query.strip().lower()}%"
        stmt = (
            select(Document)
            .where(
                Document.owner_id == owner_id,
                or_(
                    func.lower(Document.original_filename).like(term),
                    func.lower(Document.file_extension).like(term),
                    func.lower(Document.mime_type).like(term)
                )
            )
            .order_by(Document.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def paginate(
        self,
        owner_id: uuid.UUID,
        page: int = 1,
        page_size: int = 20,
        search_query: Optional[str] = None
    ) -> Tuple[List[Document], int]:
        """
        Returns paginated list of documents alongside total count.
        
        :return: Tuple of (document_list, total_count)
        """
        page = max(1, page)
        page_size = max(1, min(100, page_size))
        skip = (page - 1) * page_size

        if search_query and search_query.strip():
            items = await self.search(owner_id, search_query.strip(), skip=skip, limit=page_size)
            total = await self.count_documents(owner_id, search_term=search_query.strip())
        else:
            items = await self.list_documents(owner_id, skip=skip, limit=page_size)
            total = await self.count_documents(owner_id)

        return items, total

    async def update_status(self, doc: Document, status: str) -> Document:
        """Updates document processing status."""
        doc.upload_status = status
        self.db.add(doc)
        await self.db.flush()
        await self.db.refresh(doc)
        return doc

    async def delete(self, doc: Document) -> None:
        """Deletes document entity from database."""
        await self.db.delete(doc)
        await self.db.flush()
