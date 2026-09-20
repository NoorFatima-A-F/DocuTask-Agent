"""
Database Setup & SQLAlchemy 2.0 Declarative Base for Enterprise Verification Platform.
"""
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator


class VerificationBase(DeclarativeBase):
    pass


# Default SQLite Async for in-memory & test isolation, easily configurable to PostgreSQL asyncpg
TEST_DB_URL = "sqlite+aiosqlite:///:memory:"
verification_engine = create_async_engine(TEST_DB_URL, echo=False)
VerificationAsyncSessionLocal = async_sessionmaker(
    bind=verification_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_verification_db() -> AsyncGenerator[AsyncSession, None]:
    async with VerificationAsyncSessionLocal() as session:
        yield session
