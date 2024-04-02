from fastapi.testclient import TestClient
from fastapi import status
from app.core.settings import settings


def test_get_current_user_skills(client: TestClient, user_token_headers):
    r = client.get(
        f"{settings.PROJECT_ENDPOINT_VERSION}/get_user_skills",
        headers=user_token_headers,
    )
    response = r.json()
    assert r.status_code == status.HTTP_200_OK
    assert isinstance(response, dict)


def test_add_skill_to_user(client: TestClient, user_token_headers):
    r = client.get(
        f"{settings.PROJECT_ENDPOINT_VERSION}/get_user_skills",
        headers=user_token_headers,
    )
    prev_skills_response = r.json()["items"]
    r = client.put(
        f"{settings.PROJECT_ENDPOINT_VERSION}/update_skill",
        json=prev_skills_response,
        headers=user_token_headers,
    )
    assert r.status_code == status.HTTP_201_CREATED
    r = client.get(
        f"{settings.PROJECT_ENDPOINT_VERSION}/get_user_skills",
        headers=user_token_headers,
    )
    after_skills_response = r.json()["items"]
    assert prev_skills_response == after_skills_response


def test_get_every_skills(client: TestClient, user_token_headers):
    r = client.get(
        f"{settings.PROJECT_ENDPOINT_VERSION}/get_skills", headers=user_token_headers
    )
    response = r.json()
    assert isinstance(response, dict)
    assert "items" in response
    assert isinstance(response["items"], list)
    assert "page" in response
    assert "pages" in response
    assert "size" in response
    assert r.status_code == status.HTTP_200_OK
    r = client.get(
        f"{settings.PROJECT_ENDPOINT_VERSION}/get_skills?page=-100",
        headers=user_token_headers,
    )
    assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_unadded_skills_of_user_by_query(client: TestClient, user_token_headers):
    r = client.get(
        f"{settings.PROJECT_ENDPOINT_VERSION}/get_unadded_skills",
        headers=user_token_headers,
    )
    response = r.json()
    assert isinstance(response, dict)
    assert "items" in response
    assert isinstance(response["items"], list)
    assert "page" in response
    assert "pages" in response
    assert "size" in response
    assert r.status_code == status.HTTP_200_OK
    r = client.get(
        f"{settings.PROJECT_ENDPOINT_VERSION}/get_unadded_skills?page=-100",
        headers=user_token_headers,
    )
    assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_user_by_filter(client: TestClient, user_token_headers):
    r = client.get(
        f"{settings.PROJECT_ENDPOINT_VERSION}/get_user_by_filter",
        headers=user_token_headers,
    )
    assert r.status_code == 200
    response = r.json()
    assert isinstance(response, dict)
    assert "items" in response
    assert isinstance(response["items"], list)
    assert "page" in response
    assert "pages" in response
    assert "size" in response
