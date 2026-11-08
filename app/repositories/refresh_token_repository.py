"""
RefreshTokenRepository Data Persistence Layer.
Implements token persistence and revocation operations using SQLAlchemy 2.0 async queries.
"""

import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_token import RefreshToken
from app.repositories.base import BaseRepository


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    """Repository handling persistence operations for RefreshToken entity."""

    def __init__(self, db: AsyncSession):
        super().__init__(model=RefreshToken, db=db)

    async def create(self, token_data: dict[str, Any]) -> RefreshToken:
        """Persists a new refresh token record."""
        token_obj = RefreshToken(**token_data)
        self.db.add(token_obj)
        await self.db.flush()
        await self.db.refresh(token_obj)
        return token_obj

    async def revoke(self, token_obj: RefreshToken) -> None:
        """Revokes a specific refresh token."""
        token_obj.revoked = True
        self.db.add(token_obj)
        await self.db.flush()

    async def revoke_all_for_user(self, user_id: uuid.UUID) -> None:
        """Revokes all active refresh tokens associated with a given user ID."""
        await self.db.execute(
            update(RefreshToken)
            .where(RefreshToken.user_id == user_id, RefreshToken.revoked.is_(False))
            .values(revoked=True)
        )
        await self.db.flush()

    async def get_valid_token(self, token_hash: str) -> RefreshToken | None:
        """
        Retrieves a refresh token record matching the token hash
        that is not revoked and has not expired.
        """
        now = datetime.now(UTC)
        result = await self.db.execute(
            select(RefreshToken).where(
                RefreshToken.token_hash == token_hash, RefreshToken.revoked.is_(False), RefreshToken.expires_at > now
            )
        )
        return result.scalar_one_or_none()
