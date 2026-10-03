"""
Pytest Async Configuration and Shared Fixtures.
Sets up isolated in-memory SQLite database and httpx AsyncClient.
"""

import asyncio
from typing import Any, AsyncGenerator
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
    from app.database.base import Base
    from app.database.session import get_db

    TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

    test_engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        future=True
    )

    TestAsyncSessionLocal = async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False
    )
except ImportError:
    AsyncSession, async_sessionmaker, create_async_engine = None, None, None
    Base, get_db = None, None
    test_engine, TestAsyncSessionLocal = None, None

try:
    from app.main import app
except ImportError:
    app = None


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@async_fixture(scope="function")
async def db_session() -> AsyncGenerator[Any, None]:
    """Provides a clean in-memory database session per test function."""
    if test_engine is None or Base is None:
        yield None
        return
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestAsyncSessionLocal() as session:
        yield session
        await session.rollback()

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@async_fixture(scope="function")
async def client(db_session: Any) -> AsyncGenerator[Any, None]:
    """Provides an AsyncClient bound to app with overridden database session dependency."""
    if ASGITransport is None or AsyncClient is None:
        yield None
        return

    async def _override_get_db() -> AsyncGenerator[Any, None]:
        yield db_session

    if get_db is not None:
        app.dependency_overrides[get_db] = _override_get_db
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
        
    app.dependency_overrides.clear()

