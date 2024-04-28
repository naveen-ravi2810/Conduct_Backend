"""Conftest for the application"""

from typing import Generator
import asyncio
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
import pytest_asyncio

from main import app
from app.core.settings import settings
from app.core.db import get_session
from app.core.security import hash_password
from app.models import Users, SQLModel

# Initilizing the engine and session
engine_test: AsyncEngine = create_async_engine(settings.TEST_DB_URI)
async_session_maker = async_sessionmaker(
    bind=engine_test,
    class_=AsyncSession,
    expire_on_commit=False,
)


# yielding session
async def override_get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


# Dependency_overriding
app.dependency_overrides[get_session] = override_get_session


# Test data loading
new_user_data = {
    "email": "test.r2021eceb@sece.ac.in",
    "year": 2025,
    "phone": "8903711336",
    "name": "test_user",
    "password": hash_password("test@1234"),
}


# Event loop to avoid Future pending error
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    res = asyncio.new_event_loop()
    asyncio.set_event_loop(res)
    res._close = res.close
    res.close = lambda: None
    yield res
    res._close()


# making tables and inserting sample data with order1
@pytest.mark.order1
@pytest.fixture(scope="session", autouse=True)
async def create_tables():
    async with engine_test.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    async with async_session_maker() as session:
        new_user = Users(**new_user_data)
        session.add(new_user)
        await session.commit()
        yield
        await asyncio.sleep(5)
        await session.delete(new_user)
        await session.commit()
    async with engine_test.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


# yeilding async client
@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(app=app, base_url=f"http://test") as client:
        yield client
