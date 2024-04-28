from httpx import AsyncClient
from app.core.settings import settings
from main import app
import pytest


@pytest.mark.asyncio
async def test_health_check(async_client: AsyncClient):
    r = await async_client.get("/health")
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        r = await async_client.post(
            f"{settings.PROJECT_ENDPOINT_VERSION}/login",
            json={"email": "test.r2021eceb@sece.ac.in", "password": "test@1234"},
        )
        response = r.json()
        print(r.json())
        assert r.status_code == 200
        assert 1 == 1
