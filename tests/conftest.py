"""
Pytest Async Configuration and Shared Fixtures.
Sets up isolated in-memory SQLite database, httpx AsyncClient, and mocked core dependencies.
"""

import asyncio
from typing import Any, AsyncGenerator
from unittest.mock import AsyncMock, MagicMock
import pytest

try:
    import pytest_asyncio

    async_fixture = pytest_asyncio.fixture
except ImportError:
    async_fixture = pytest.fixture

try:
    from httpx import ASGITransport, AsyncClient
except ImportError:
    ASGITransport, AsyncClient = None, None

try:
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
    from sqlalchemy.pool import StaticPool
    from app.database.base import Base
    from app.database.session import get_db
    import app.database.session as app_session
except ImportError:
    AsyncSession, async_sessionmaker, create_async_engine = None, None, None
    StaticPool = None
    Base, get_db, app_session = None, None, None

try:
    from app.main import app
except ImportError:
    app = None


@async_fixture(scope="function")
async def db_session() -> AsyncGenerator[Any, None]:
    """Provides a clean in-memory database session per test function."""
    if Base is None or create_async_engine is None or StaticPool is None:
        yield MagicMock()
        return

    test_engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
        future=True,
    )
    test_session_maker = async_sessionmaker(
        bind=test_engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
    )

    old_engine = app_session.engine if app_session else None
    old_session_local = app_session.AsyncSessionLocal if app_session else None

    if app_session:
        app_session.engine = test_engine
        app_session.AsyncSessionLocal = test_session_maker

    try:
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        async with test_session_maker() as session:
            yield session
            await session.rollback()

        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
    finally:
        if app_session:
            app_session.engine = old_engine
            app_session.AsyncSessionLocal = old_session_local
        await test_engine.dispose()


@async_fixture(scope="function")
async def client(db_session: Any) -> AsyncGenerator[Any, None]:
    """Provides an AsyncClient bound to app with overridden database session dependency."""
    if ASGITransport is None or AsyncClient is None or app is None:
        yield MagicMock()
        return

    async def _override_get_db() -> AsyncGenerator[Any, None]:
        yield db_session

    if get_db is not None:
        app.dependency_overrides[get_db] = _override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
def mock_redis():
    """Mock Redis client for testing."""
    redis_mock = AsyncMock()
    redis_mock.get.return_value = None
    redis_mock.set.return_value = True
    redis_mock.delete.return_value = True
    redis_mock.exists.return_value = False
    return redis_mock


@pytest.fixture
def mock_celery():
    """Mock Celery app for testing."""
    celery_mock = MagicMock()
    celery_mock.send_task.return_value = MagicMock(id="mock-task-id")
    return celery_mock
