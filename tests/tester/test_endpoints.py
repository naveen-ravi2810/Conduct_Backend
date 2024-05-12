from httpx import AsyncClient
from app.core.settings import settings
from app.core.init_db import new_user_data_1, new_user_data_3, new_user_data_2
from app.core.db import r_conn
import pytest


async def test_health_check(async_client: AsyncClient):
    r = await async_client.get("/health")
    assert r.status_code == 200


async def test_create_user(async_client: AsyncClient):
    # Set a otp in redis to check for adding new user to the database
    await r_conn.setex(
        name=f"register_otp:{new_user_data_3['email']}", value="000000", time=600
    )
    r = await async_client.post(
        f"{settings.PROJECT_ENDPOINT_VERSION}/register",
        json={
            "name": new_user_data_3["name"],
            "phone": new_user_data_3["phone"],
            "password": new_user_data_3["password"],
            "email": new_user_data_3["email"],
            "year": "2025",
            "otp": "000000",
        },
    )
    assert r.status_code == 201


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


async def test_token(async_client: AsyncClient):
    r = await async_client.get(
        f"{settings.PROJECT_ENDPOINT_VERSION}/token",
        headers={"Authorization": f"Bearer {pytest.token}"},
    )
    response = r.json()
    pytest.email = response["email"]
    assert r.status_code == 200
    assert response["message"] == "Token Validated"
    assert "message" in response
    assert "email" in response
    assert "id" in response
    assert response["status"] == True


async def test_get_own_profile(async_client: AsyncClient):
    r = await async_client.get(
        f"{settings.PROJECT_ENDPOINT_VERSION}/profile/{pytest.id_1}",
        headers={"Authorization": f"Bearer {pytest.token}"},
    )
    response = r.json()
    assert r.status_code == 200
    assert response["year"] == new_user_data_1["year"]
    assert response["phone"] == new_user_data_1["phone"]
    assert response["email"] == new_user_data_1["email"]


async def test_get_other_profile(async_client: AsyncClient):
    r = await async_client.get(
        f"{settings.PROJECT_ENDPOINT_VERSION}/profile/{pytest.id_2}",
        headers={"Authorization": f"Bearer {pytest.token}"},
    )
    response = r.json()
    assert r.status_code == 200
    assert response["year"] == new_user_data_2["year"]
    assert (
        response["phone"][0:5] == new_user_data_2["phone"][0:5]
    )  # Other user phone will be hashed for last 5 numbers
    assert response["email"] == new_user_data_2["email"]


async def test_both_update_get_uri(async_client: AsyncClient):
    r = await async_client.put(
        f"{settings.PROJECT_ENDPOINT_VERSION}/update_user",
        json={
            "github_uri": "https://github.com/test_user_1",
            "linkedin_uri": "https://linkedin.com/test_user_1/12345678",
            "leetcode_uri": None,
            "codechef_uri": None,
            "portfolio_uri": None,
            "description": None,
        },
        headers={"Authorization": f"Bearer {pytest.token}"},
    )
    response = r.json()
    assert r.status_code == 202
    assert response["github_uri"] == "https://github.com/test_user_1"
    assert response["linkedin_uri"] == "https://linkedin.com/test_user_1/12345678"
    assert response["leetcode_uri"] == None


async def test_get_uri_of_the_user(async_client: AsyncClient):
    r = await async_client.get(
        f"{settings.PROJECT_ENDPOINT_VERSION}/update_uri",
        headers={"Authorization": f"Bearer {pytest.token}"},
    )
    response = r.json()
    assert r.status_code == 200
    assert response["github_uri"] == "https://github.com/test_user_1"
    assert response["linkedin_uri"] == "https://linkedin.com/test_user_1/12345678"
    assert response["leetcode_uri"] == None


async def test_logout(async_client: AsyncClient):
    r = await async_client.delete(
        f"{settings.PROJECT_ENDPOINT_VERSION}/logout",
        headers={"Authorization": f"Bearer {pytest.token}"},
    )
    response = r.json()
    assert response["status"] == "ok"
    assert response["message"] == "User Logout Successfully"
