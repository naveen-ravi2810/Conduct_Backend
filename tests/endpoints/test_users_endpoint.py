"""
Test for users endpoint
"""

from fastapi.testclient import TestClient
from app.core.settings import settings


def test_current_users(client: TestClient, user_token_headers):
    r = client.get(
        f"{settings.PROJECT_ENDPOINT_VERSION}/profile/06609ab0-d008-7bf0-8000-a504a6f2f4d6",
        headers=user_token_headers,
    )
    assert r.status_code == 200
    response = r.json()
    assert response["curr_user"] is True
    assert response["id"] == "06609ab0-d008-7bf0-8000-a504a6f2f4d6"


def test_other_user(client: TestClient, user_token_headers):
    r = client.get(
        f"{settings.PROJECT_ENDPOINT_VERSION}/profile/0", headers=user_token_headers
    )
    assert r.status_code == 404
    response = r.json()
    assert response["detail"] == "User Not found"


def test_update_uri(client: TestClient, user_token_headers):
    r = client.get(
        f"{settings.PROJECT_ENDPOINT_VERSION}/update_uri", headers=user_token_headers
    )
    response = r.json()
    assert r.status_code == 200
    assert "github_uri" in response
    assert "linkedin_uri" in response
    assert "leetcode_uri" in response
    assert "codechef_uri" in response
    assert "portfolio_uri" in response
    assert "description" in response


def test_token(client: TestClient, user_token_headers):
    r = client.get(
        f"{settings.PROJECT_ENDPOINT_VERSION}/token", headers=user_token_headers
    )
    response = r.json()
    assert "X-Time-Elapsed" in r.headers
    assert r.status_code == 200
    assert response["message"] == "Token Validated"


def test_get_update_user(client: TestClient, user_token_headers):
    r = client.put(
        f"{settings.PROJECT_ENDPOINT_VERSION}/update_user",
        json={"description": "None"},
        headers=user_token_headers,
    )
    response = r.json()
    assert r.status_code == 202
    assert "github_uri" in response
    assert "linkedin_uri" in response
    assert "leetcode_uri" in response
    assert response["description"] == "None"


def test_email_verification(client: TestClient):
    r = client.get(
        f"{settings.PROJECT_ENDPOINT_VERSION}/email_verification?email=testabc@example.com"
    )
    response = r.json()
    assert r.status_code == 400
    assert response["detail"] == f"Email must end with {settings.EMAIL_DOMAIN}"


def test_register(client: TestClient):
    r = client.post(
        f"{settings.PROJECT_ENDPOINT_VERSION}/register",
        json={
            "name": "Naveen Ravi",
            "phone": "1234567890",
            "password": "Your_strong_password",
            "email": "test.a2021eceb@sece.ac.in",
            "year": "2025",
            "otp": "123456",
        },
    )
    response = r.json()
    assert r.status_code != 200
    assert r.status_code == 409
    assert response["detail"] == "Invalid OTP"
