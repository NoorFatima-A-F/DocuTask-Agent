"""
Unit Tests for Database Repositories Layer.
"""

from datetime import datetime, timedelta, timezone
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository


@pytest.mark.asyncio
async def test_user_repository_crud(db_session: AsyncSession):
    """Tests UserRepository CRUD persistence operations."""
    repo = UserRepository(db_session)

    # 1. Create user
    user_data = {
        "email": "repo_test@example.com",
        "username": "repotest",
        "hashed_password": "hashed_secret_password",
        "is_active": True,
        "is_superuser": False
    }
    user = await repo.create(user_data)
    assert user.id is not None
    assert user.email == "repo_test@example.com"

    # 2. Exists checks
    assert await repo.exists_email("repo_test@example.com") is True
    assert await repo.exists_email("nonexistent@example.com") is False
    assert await repo.exists_username("repotest") is True

    # 3. Getters
    by_email = await repo.get_by_email("REPO_TEST@example.com")
    assert by_email is not None and by_email.id == user.id

    by_username = await repo.get_by_username("REPOTEST")
    assert by_username is not None and by_username.id == user.id

    by_id = await repo.get_by_id(user.id)
    assert by_id is not None and by_id.username == "repotest"

    # 4. Update
    updated_user = await repo.update(user, {"is_active": False})
    assert updated_user.is_active is False

    # 5. Delete
    await repo.delete(updated_user)
    assert await repo.get_by_id(user.id) is None


@pytest.mark.asyncio
async def test_refresh_token_repository_operations(db_session: AsyncSession):
    """Tests RefreshTokenRepository token management operations."""
    user_repo = UserRepository(db_session)
    token_repo = RefreshTokenRepository(db_session)

    # Setup User
    user = await user_repo.create({
        "email": "token_repo_test@example.com",
        "username": "tokenrepotest",
        "hashed_password": "hashed_secret",
    })

    # 1. Create Refresh Token
    token_hash = "mock_sha256_hash_value_1234567890"
    expires_at = datetime.now(timezone.utc) + timedelta(days=7)
    token_obj = await token_repo.create({
        "user_id": user.id,
        "token_hash": token_hash,
        "expires_at": expires_at,
        "revoked": False
    })
    assert token_obj.id is not None

    # 2. Retrieve valid token
    fetched = await token_repo.get_valid_token(token_hash)
    assert fetched is not None
    assert fetched.id == token_obj.id

    # 3. Revoke token
    await token_repo.revoke(token_obj)
    fetched_after_revoke = await token_repo.get_valid_token(token_hash)
    assert fetched_after_revoke is None

    # 4. Create multiple tokens and revoke_all_for_user
    t1 = await token_repo.create({
        "user_id": user.id,
        "token_hash": "hash_1",
        "expires_at": expires_at,
        "revoked": False
    })
    t2 = await token_repo.create({
        "user_id": user.id,
        "token_hash": "hash_2",
        "expires_at": expires_at,
        "revoked": False
    })

    await token_repo.revoke_all_for_user(user.id)
    assert await token_repo.get_valid_token("hash_1") is None
    assert await token_repo.get_valid_token("hash_2") is None
