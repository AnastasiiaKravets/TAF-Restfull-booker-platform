import pytest

from src.API.models.auth_models import AuthResponse
from src.API.models.common_models import BasicErrorResponse
from src.API.models.user_models import UserResponse
from src.utils.API_utils import get_valid_user


@pytest.mark.api
def test_authorize_valid_user(api_client):
    user = get_valid_user()

    response = api_client.post('auth/login', payload=user)

    assert response.status_code == 200
    auth_response = AuthResponse.model_validate(response.json())
    assert auth_response.username == user.username


@pytest.mark.api
@pytest.mark.parametrize('credentials_override, error_message',
                         [({'username': ''}, 'Username and password required'),
                          ({'password': ''}, 'Username and password required'),
                          ({'username': '78979'}, 'Invalid credentials'),
                          ({'password': '123'}, 'Invalid credentials')])
def test_authorize_user_with_invalid_credentials(api_client, credentials_override, error_message):
    user = get_valid_user(**credentials_override)

    response = api_client.post('auth/login', payload=user)

    assert response.status_code == 400
    error_response = BasicErrorResponse.model_validate(response.json())
    assert error_response.message == error_message


@pytest.mark.api
def test_get_authorized_user(authorized_api_client):
    user = get_valid_user()
    response = authorized_api_client.get('auth/me')

    assert response.status_code == 200
    user_data = UserResponse.model_validate(response.json())
    assert user_data.username == user.username
