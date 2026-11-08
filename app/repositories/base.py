"""
Base Repository Interface.
Defines foundational repository patterns for SQLAlchemy AsyncSession.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import Base


class BaseRepository[ModelType: Base]:
    """Generic base repository for CRUD database operations."""

    def __init__(self, model: type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db
