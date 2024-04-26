from httpx import AsyncClient
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
import pytest

from main import app
from app.core.settings import settings
from app.core.db import get_session
from app.core.security import hash_password
from app.models import *

engine_test = create_async_engine(settings.TEST_DB_URI)
async_session_maker = async_sessionmaker(
    engine_test,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

new_user_data = {
    "email":"test.r2021eceb@sece.ac.in",
    "year":2025,
    "phone":"8903711436",
    "name":"test_user",
    "password": hash_password("test@1234")
}

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
        # await conn.run_sync(SQLModel.metadata.drop_all)

# @pytest.fixture(autouse=True)
# async def create_test_user():
   


async def override_get_session():
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_session] = override_get_session


# @pytest.fixture(scope="session")
# async def async_client() -> AsyncGenerator[AsyncClient, None]:
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         yield ac


from fastapi.testclient import TestClient
@pytest.fixture(scope="session")
def client() :
    with TestClient(app=app, base_url="http://test") as ac:
        yield ac

# @pytest.mark.asyncio
# @pytest.fixture(scope="session")
# async def test_login(async_client: AsyncClient):
#     r = await async_client.post(
#         f"{settings.PROJECT_ENDPOINT_VERSION}/login",
#         json={"email": "naveen.r2021eceb@sece.ac.in", "password": "test@1234"},
#     )
#     response = r.json()
#     user_token = response["access_token"]
#     yield {"Authorization": f"Bearer {user_token}"}
