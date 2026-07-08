import pytest

from config import settings
from src.API.API_Client import API_Client
from src.API.models.auth_models import AuthRequest, AuthResponse


@pytest.fixture(scope="module")
def api_client():
    with API_Client() as client:
        yield client

@pytest.fixture(scope="module")
def authorized_api_client(api_client, get_valid_user):
    response = api_client.post('auth/login', json=get_valid_user.model_dump())
    auth_response = AuthResponse.model_validate(response.json())
    headers = {'Authorization': f'Bearer {auth_response.accessToken}'}
    with API_Client(headers=headers) as auth_client:
        yield auth_client


@pytest.fixture(scope="module")
def get_valid_user():
    user = {'username': settings.TEST_API_USERNAME, 'password': settings.TEST_API_PASSWORD}
    return AuthRequest(**user)