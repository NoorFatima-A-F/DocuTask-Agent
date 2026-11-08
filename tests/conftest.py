"""Shared fixtures: an isolated in-memory database per test and an HTTP client bound to the app.

Imports are unconditional on purpose: if the app cannot be imported, every test must fail
rather than silently run against mocks.
"""

from collections.abc import AsyncGenerator, Iterator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

import app.database.session as app_session
from app.database.base import Base
from app.database.session import get_db
from app.main import app
from app.middleware.rate_limit import rate_limiter


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """A clean in-memory SQLite database; the app's session factory points at it for the test."""
    test_engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    test_session_maker = async_sessionmaker(
        bind=test_engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
    )
    old_engine, old_session_local = app_session.engine, app_session.AsyncSessionLocal
    app_session.engine, app_session.AsyncSessionLocal = test_engine, test_session_maker
    try:
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        async with test_session_maker() as session:
            yield session
            await session.rollback()
    finally:
        app_session.engine, app_session.AsyncSessionLocal = old_engine, old_session_local
        await test_engine.dispose()


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """AsyncClient bound to the app, sharing ``db_session`` with the request handlers."""

    async def _override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def _reset_rate_limiter() -> Iterator[None]:
    """Each test starts with empty in-process rate-limit counters (no Redis)."""
    rate_limiter.memory.clear()
    saved, rate_limiter.redis = rate_limiter.redis, None
    yield
    rate_limiter.redis = saved
