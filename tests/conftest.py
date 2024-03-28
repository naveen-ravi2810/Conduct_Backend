from fastapi.testclient import TestClient
from collections.abc import Generator
import pytest

from .utils.utils import (
    get_user_token_headers
)
from main import app


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app=app) as c:
        yield c


@pytest.fixture(scope="module")
def user_token_headers(client: TestClient) -> dict[str, str]:
    return get_user_token_headers(client)
