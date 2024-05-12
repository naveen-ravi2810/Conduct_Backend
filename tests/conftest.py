"""Conftest for the application"""

import asyncio
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
import pytest_asyncio

from main import app
from app.core.init_db import (
    add_main_skills,
    original_final,
    new_user_data_1,
    new_user_data_2,
)
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


# # yielding session
async def override_get_session() -> AsyncSession:  # type: ignore
    async with async_session_maker() as session:
        yield session


# # Dependency_overriding
app.dependency_overrides[get_session] = override_get_session


# Test data loading


# Event loop to avoid Future pending error
@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


# making tables and inserting sample data with order1
@pytest.mark.order1
@pytest.fixture(scope="session", autouse=True)
async def create_tables():
    async with engine_test.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    async with async_session_maker() as session:
        new_user_1 = Users(**new_user_data_1)
        new_user_2 = Users(**new_user_data_2)
        session.add(new_user_1)
        session.add(new_user_2)
        await session.commit()
        await add_main_skills(session=session, skills=original_final)
        yield
    async with engine_test.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


# yeilding async client
@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(app=app, base_url=f"http://test") as client:
        yield client
