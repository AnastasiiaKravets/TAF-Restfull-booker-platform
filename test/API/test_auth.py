import pytest

from src.API.models.auth_models import AuthRequest, AuthResponse
from src.API.models.common_models import BasicErrorResponse
from src.API.models.user_models import UserResponseModel


@pytest.mark.api
def test_authorize_valid_user(api_client, get_valid_user):
    response = api_client.post('auth/login', json=get_valid_user.model_dump())
    auth_response = AuthResponse.model_validate(response.json())

    assert response.status_code == 200
    assert auth_response.username == get_valid_user.username

@pytest.mark.api
@pytest.mark.parametrize('override, error_message',
                         [({'username': ''}, 'Username and password required'),
                          ({'password': ''}, 'Username and password required'),
                          ({'username': '78979'}, 'Invalid credentials'),
                          ({'password': '123'}, 'Invalid credentials')])
def test_authorize_user_invalid(api_client, override, error_message):
    user = {'username': 'emilys1', 'password': 'emilyspass1'}
    user.update(override)
    response = api_client.post('auth/login', json=AuthRequest(**user).model_dump())

    assert response.status_code == 400

    auth_response = BasicErrorResponse.model_validate(response.json())
    assert auth_response.message == error_message

@pytest.mark.api
def test_get_authorized_user(authorized_api_client, get_valid_user):
    response = authorized_api_client.get('auth/me')

    assert response.status_code == 200
    user_data = UserResponseModel.model_validate(response.json())
    assert user_data.username == get_valid_user.username
