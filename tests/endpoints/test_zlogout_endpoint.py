from fastapi.testclient import TestClient
from app.core.settings import settings


def test_logout(client: TestClient, user_token_headers):
    r = client.delete(
        f"{settings.PROJECT_ENDPOINT_VERSION}/logout", headers=user_token_headers
    )
    response = r.json()
    assert r.status_code == 200
    assert response["message"] == "User Logout Successfully"
    assert response["status"] == "ok"


def test_user_after_logout(client: TestClient, user_token_headers):
    r = client.get(
        f"{settings.PROJECT_ENDPOINT_VERSION}/profile/1", headers=user_token_headers
    )
    assert r.status_code == 401
