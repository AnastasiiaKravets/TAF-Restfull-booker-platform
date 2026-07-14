from src.API.restfull_booker_service.models.auth_models import AuthResponse
from src.API.restfull_booker_service.models.common_models import BasicErrorResponse


def get_valid_user():
    return {'username': 'admin', 'password': 'password'}


def test_login_valid_credentials(api_client):
    response = api_client.post('auth/login', payload=get_valid_user())
    assert response.status_code == 200
    AuthResponse.model_validate(response.json())


def test_login_invalid_credentials(api_client):
    user = {'username': '', 'password': ''}
    response = api_client.post('auth/login', payload=user)
    assert response.status_code == 401
    error_response = BasicErrorResponse.model_validate(response.json())
    assert error_response.error == 'Invalid credentials'


def test_validate(authorized_api_client, token):
    print(token)
    print(authorized_api_client.client.headers)
    payload = {'token': token}
    response = authorized_api_client.post('auth/validate', payload=payload)
    print(response.text)
    assert response.status_code == 200


def test_logout(authorized_api_client, token):
    payload = {'token': token}
    response = authorized_api_client.post('auth/logout', payload=payload)
    print(response.text)
    assert response.status_code == 200
