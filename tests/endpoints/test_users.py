from httpx import AsyncClient
from app.core.settings import settings
from app.core.init_db import new_user_data_1, new_user_data_2
import pytest


@pytest.mark.asyncio
async def test_health_check(async_client: AsyncClient):
    r = await async_client.get("/health")
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_login(async_client: AsyncClient):
    r = await async_client.post(
        f"{settings.PROJECT_ENDPOINT_VERSION}/login",
        json={"email": f"{new_user_data_1['email']}", "password": "test@1234"},
    )
    response = r.json()
    pytest.token = response["access_token"]  # Storing value in pytest
    assert r.status_code == 200
    assert "access_token" in response
    assert response["status"] == True


@pytest.mark.asyncio
async def test_token(async_client: AsyncClient):
    r = await async_client.get(
        f"{settings.PROJECT_ENDPOINT_VERSION}/token",
        headers={"Authorization": f"Bearer {pytest.token}"},
    )
    response = r.json()
    pytest.id = response["id"]
    pytest.email = response["email"]
    assert r.status_code == 200
    assert response["message"] == "Token Validated"
    assert "message" in response
    assert "email" in response
    assert "id" in response
    assert response["status"] == True


@pytest.mark.asyncio
async def test_get_own_profile(async_client: AsyncClient):
    r = await async_client.get(
        f"{settings.PROJECT_ENDPOINT_VERSION}/profile/{pytest.id}",
        headers={"Authorization": f"Bearer {pytest.token}"},
    )
    response = r.json()
    assert r.status_code == 200
    assert response["phone"] == new_user_data_1["phone"]
    assert response["email"] == pytest.email


@pytest.mark.asyncio
async def test_logout(async_client: AsyncClient):
    r = await async_client.delete(
        f"{settings.PROJECT_ENDPOINT_VERSION}/logout",
        headers={"Authorization": f"Bearer {pytest.token}"},
    )
    response = r.json()
    assert response["status"] == "ok"
    assert response["message"] == "User Logout Successfully"
