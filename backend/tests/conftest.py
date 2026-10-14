"""Pytest fixtures for testing.

Unit tests (enums, schemas) do NOT require a database.
Integration tests (models, api, repo, service) require it via the
db_session or client fixtures, which pull in the DB setup on demand.
"""
from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from landslide_backend.config import settings
from landslide_backend.database import Base, get_db
from landslide_backend.main import app


TEST_DATABASE_URL = settings.database_url

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    pool_pre_ping=False,
)


@pytest.fixture(scope="session")
def event_loop():
    """Single event loop for the whole test session (needed for asyncpg)."""
    import asyncio
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def setup_schema():
    """Create schema once per session. Only pulled in by db_session."""
    async with test_engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest.fixture
async def db_session(setup_schema) -> AsyncGenerator[AsyncSession, None]:
    """
    Transaction-per-test isolation using SAVEPOINTs.

    Every `session.commit()` inside a test becomes a savepoint release,
    which the outer transaction rollback can undo. This means tests cannot
    leak state to each other, even though they call commit() internally.
    """
    async with test_engine.connect() as connection:
        transaction = await connection.begin()
        session = AsyncSession(
            bind=connection,
            expire_on_commit=False,
            join_transaction_mode="create_savepoint",
        )
        try:
            yield session
        finally:
            await session.close()
            await transaction.rollback()


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """HTTP client that shares the test's db_session."""
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
