# from httpx import AsyncClient
# import pytest

# from app.core.settings import settings


# @pytest.mark.asyncio
# async def test_login(async_client: AsyncClient, get_header):
#     response = await async_client.get(
#         f"{settings.PROJECT_ENDPOINT_VERSION}/profile/b70eab2b-4ed2-4778-a987-e9336d4d07ab",
#         headers=get_header
#     )
#     print(response.json())
#     assert response.status_code == 200
#     print(response.json())

from httpx import AsyncClient
from app.core.settings import settings
import pytest

# @pytest.mark.anyio
# async def test_login(async_client: AsyncClient):
#     r = await async_client.post(
#         f"{settings.PROJECT_ENDPOINT_VERSION}/login",
#         json={"email": "naveen.r2021eceb@sece.ac.in", "password": "test@1234"},
#     )
#     response = r.json()
#     # user_token = response["access_token"]
#     # yield {"Authorization": f"Bearer {user_token}"}
#     print(r.json())
#     assert r.status_code == 200

def test_login(client):
    r = client.post(
        f"{settings.PROJECT_ENDPOINT_VERSION}/login",
        json={"email": "naveen.r2021eceb@sece.ac.in", "password": "test@1234"},
    )
    response = r.json()
    # user_token = response["access_token"]
    # yield {"Authorization": f"Bearer {user_token}"}
    print(r.json())
    assert r.status_code == 200