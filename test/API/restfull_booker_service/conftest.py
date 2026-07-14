import pytest

from config import settings
from src.API.API_Client import API_Client
from src.API.restfull_booker_service.models.auth_models import AuthResponse


@pytest.fixture(scope="package")
def api_client():
    with API_Client(base_url=settings.RESTFULL_BASE_API_URL) as client:
        yield client


@pytest.fixture(scope="module")
def authorized_api_client(api_client):
    response = api_client.post('auth/login', payload={'username': 'admin', 'password': 'password'})
    auth_response = AuthResponse.model_validate(response.json())
    headers = {'Cookie': f'token={auth_response.token}'}
    with API_Client(base_url=settings.RESTFULL_BASE_API_URL, headers=headers) as auth_client:
        yield auth_client


@pytest.fixture(scope="module")
def token(authorized_api_client):
    yield authorized_api_client.client.headers['Cookie'][6:]
