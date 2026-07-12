import pytest

from src.API.API_Client import API_Client
from src.API.models.auth_models import AuthResponse
from src.utils.API_utils import get_valid_user


@pytest.fixture(scope="module")
def api_client():
    with API_Client() as client:
        yield client

@pytest.fixture(scope="module")
def authorized_api_client(api_client):
    response = api_client.post('auth/login', payload=get_valid_user())
    auth_response = AuthResponse.model_validate(response.json())
    headers = {'Authorization': f'Bearer {auth_response.accessToken}'}
    with API_Client(headers=headers) as auth_client:
        yield auth_client
