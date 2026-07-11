import pytest

from src.API.models.cart_models import CartListResponse, CartResponse, DeletedCartResponse
from src.API.models.common_models import BasicErrorResponse
from src.utils.API_utils import get_random_id, get_cart_payload
from src.assertion_helpers.API_assertions import assert_pagination


@pytest.mark.api
def test_get_all_carts(api_client):
    response = api_client.get('carts')
    assert response.status_code == 200

    carts_response = CartListResponse.model_validate(response.json())
    assert_pagination(carts_response)
    assert len(carts_response.carts) > 0

    unique_cart_ids = set(product.id for product in carts_response.carts)
    assert len(carts_response.carts) == len(unique_cart_ids), "There is duplicate in cart ids"


@pytest.mark.api
def test_get_cart_by_id(api_client):
    cart_id = get_random_id()
    response = api_client.get(f'carts/{cart_id}')
    assert response.status_code == 200

    carts_response = CartResponse.model_validate(response.json())
    assert carts_response.id == cart_id


@pytest.mark.api
def test_get_cart_by_invalid_id(api_client):
    cart_id = get_random_id(start=100000, end=200000)
    response = api_client.get(f'carts/{cart_id}')
    assert response.status_code == 404

    error_response = BasicErrorResponse.model_validate(response.json())
    assert error_response.message == f"Cart with id '{cart_id}' not found"


@pytest.mark.api
def test_get_carts_by_user_id(api_client):
    user_id = get_random_id()
    response = api_client.get(f'carts/user/{user_id}')
    assert response.status_code == 200
    carts_response = CartListResponse.model_validate(response.json())

    assert len(carts_response.carts) > 0
    assert_pagination(carts_response)

    unique_carts_ids = set(cart.id for cart in carts_response.carts)
    assert len(carts_response.carts) == len(unique_carts_ids), "There is duplicate in cart ids"


@pytest.mark.api
def test_create_cart(api_client):
    cart_payload = get_cart_payload(user_id = get_random_id(), number_of_products=3)
    payload_product_ids = [product['id'] for product in cart_payload['products']].sort()

    response = api_client.post(f'carts/add', json=cart_payload)
    assert response.status_code == 201

    cart_response = CartResponse.model_validate(response.json())
    created_product_ids = [product.id for product in cart_response.products].sort()
    assert payload_product_ids == created_product_ids


@pytest.mark.api
def test_update_cart(api_client):
    cart_id = get_random_id()
    update_cart_payload = get_cart_payload(merge = True, number_of_products = 1)

    response = api_client.put(f'carts/{cart_id}', json=update_cart_payload)
    assert response.status_code == 200
    cart_response = CartResponse.model_validate(response.json())
    updated_product_info = [product for product in cart_response.products if product.id == update_cart_payload['products'][0]['id']]
    assert updated_product_info[0].quantity == update_cart_payload['products'][0]['quantity']


@pytest.mark.api
def test_delete_cart(api_client):
    cart_id = get_random_id()
    response = api_client.delete(f'carts/{cart_id}')
    assert response.status_code == 200
    cart_response = DeletedCartResponse.model_validate(response.json())
    assert cart_response.isDeleted == True

