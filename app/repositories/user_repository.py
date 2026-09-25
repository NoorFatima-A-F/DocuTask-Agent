"""
UserRepository Data Persistence Layer.
Implements user data access using SQLAlchemy 2.0 async queries.
"""

import uuid
from typing import Dict, Any, Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository handling persistence operations for User entity."""

    def __init__(self, db: AsyncSession):
        super().__init__(model=User, db=db)

    async def create(self, user_data: Dict[str, Any]) -> User:
        """Creates and persists a new user record."""
        user = User(**user_data)
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def get_by_email(self, email: str) -> Optional[User]:
        """Retrieves user by case-insensitive email address."""
        result = await self.db.execute(
            select(User).where(func.lower(User.email) == func.lower(email.strip()))
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[User]:
        """Retrieves user by case-insensitive username."""
        result = await self.db.execute(
            select(User).where(func.lower(User.username) == func.lower(username.strip()))
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """Retrieves user by primary key UUID."""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def exists_email(self, email: str) -> bool:
        """Checks if a user with given email exists."""
        result = await self.db.execute(
            select(func.count(User.id)).where(func.lower(User.email) == func.lower(email.strip()))
        )
        count = result.scalar() or 0
        return count > 0

    async def exists_username(self, username: str) -> bool:
        """Checks if a user with given username exists."""
        result = await self.db.execute(
            select(func.count(User.id)).where(func.lower(User.username) == func.lower(username.strip()))
        )
        count = result.scalar() or 0
        return count > 0

    async def update(self, user: User, update_data: Dict[str, Any]) -> User:
        """Updates user attributes and persists changes."""
        for field, value in update_data.items():
            if hasattr(user, field):
                setattr(user, field, value)
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def delete(self, user: User) -> None:
        """Deletes user entity from persistence."""
        await self.db.delete(user)
        await self.db.flush()
