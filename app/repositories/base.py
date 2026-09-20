"""
Base Repository Interface.
Defines foundational repository patterns for SQLAlchemy AsyncSession.
"""

from typing import Generic, Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Generic base repository for CRUD database operations."""

    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db
