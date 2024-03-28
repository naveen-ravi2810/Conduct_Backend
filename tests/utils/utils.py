from fastapi.testclient import TestClient
from app.core.settings import settings


def get_user_token_headers(client: TestClient):
    user_details = {
        "email": "naveen.r2021eceb@sece.ac.in",
        "password": "Naveen@1234",
    }
    r = client.post(
        f"{settings.PROJECT_ENDPOINT_VERSION}/login",
        headers={"Content-Type": "application/json"},
        json=user_details,
    )
    response = r.json()
    user_token = response["access_token"]
    headers = {"Authorization": f"Bearer {user_token}"}
    return headers
