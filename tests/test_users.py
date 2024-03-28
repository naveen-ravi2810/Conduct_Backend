from fastapi.testclient import TestClient
from app.core.settings import settings


def test_current_users(client: TestClient, user_token_headers):
    r = client.get(
        f"{settings.PROJECT_ENDPOINT_VERSION}/profile/1", headers=user_token_headers
    )
    assert r.status_code == 200
    response = r.json()
    assert response["curr_user"] == True
    assert response["id"] == 1


def test_other_user(client: TestClient, user_token_headers):
    r = client.get(
        f"{settings.PROJECT_ENDPOINT_VERSION}/profile/0", headers=user_token_headers
    )
    assert r.status_code == 404
    response = r.json()
    assert response["detail"] == "User Not found"
