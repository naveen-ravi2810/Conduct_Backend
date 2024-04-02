from collections.abc import Generator
from fastapi.testclient import TestClient
import pytest

from main import app
from .utils.utils import get_user_token_headers


@pytest.fixture(scope="session")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app=app) as c:
        yield c


@pytest.fixture(scope="session")
def user_token_headers(client: TestClient) -> dict[str, str]:  # pylint: disable = W0621
    return get_user_token_headers(client)
