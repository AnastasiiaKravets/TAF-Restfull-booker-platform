import random

import allure
import pytest
from faker import Faker

from src.API.models.common_models import BasicErrorResponse
from src.API.models.product_models import ProductResponse, ProductListResponse, DeletedProductResponse


@pytest.mark.api
def test_get_all_products(api_client):
    response = api_client.get('products')
    assert response.status_code == 200

    products_response = ProductListResponse.model_validate(response.json())

    assert products_response.products.__len__() > 0
    assert products_response.skip == 0
    assert products_response.limit == 30
    assert products_response.total > 0

    unique_product_ids = set(product.id for product in products_response.products)
    assert len(products_response.products) == len(unique_product_ids), "There is duplicate in product ids"

@pytest.mark.api
def test_products_paginating(api_client):
    limit = 10

    #First 10 products
    response = api_client.get('products', params={'limit': limit, 'skip': 0})
    assert response.status_code == 200
    products_response = ProductListResponse.model_validate(response.json())

    assert products_response.products.__len__() <= 10
    assert products_response.skip == 0
    assert products_response.limit == limit
    assert products_response.total > 0
    total_products_number = products_response.total

    unique_product_ids = set(product.id for product in products_response.products)
    assert len(products_response.products) == len(unique_product_ids), "There is duplicate in product ids"

    #Second 10 products
    response = api_client.get('products', params={'limit': limit, 'skip': limit})
    assert response.status_code == 200
    products_response = ProductListResponse.model_validate(response.json())

    assert products_response.products.__len__() <= 10
    assert products_response.skip == limit
    assert products_response.limit == limit
    assert products_response.total == total_products_number

    new_unique_product_ids = set(product.id for product in products_response.products)
    assert len(products_response.products) == len(new_unique_product_ids), "There is duplicate in product ids"
    assert unique_product_ids != new_unique_product_ids

    unique_product_ids.update(new_unique_product_ids)

    #Last 10 products
    skip = total_products_number - limit
    response = api_client.get('products', params={'limit': limit, 'skip': skip})
    assert response.status_code == 200
    products_response = ProductListResponse.model_validate(response.json())

    assert products_response.products.__len__() == 10
    assert products_response.skip == skip
    assert products_response.limit == limit
    assert products_response.total == total_products_number

    new_unique_product_ids = set(product.id for product in products_response.products)
    assert len(products_response.products) == len(new_unique_product_ids), "There is duplicate in product ids"
    assert unique_product_ids != new_unique_product_ids

@pytest.mark.api
def test_get_product_by_id(api_client):
    product_id = random.randint(1, 10)
    response = api_client.get(f'products/{product_id}')
    assert response.status_code == 200

    products_response = ProductResponse.model_validate(response.json())
    assert products_response.id == product_id
    # TODO add assertion with DB

@pytest.mark.api
def test_get_product_by_invalid_id(api_client):
    product_id = random.randint(100000, 200000)
    response = api_client.get(f'products/{product_id}')
    assert response.status_code == 404

    error_response = BasicErrorResponse.model_validate(response.json())
    assert error_response.message == f"Product with id '{product_id}' not found"

@pytest.mark.api
@pytest.mark.parametrize('search_word', ['phone', 'laptop', 'milk'])
def test_search_products(api_client, search_word):
    response = api_client.get('products/search', params={'q': search_word})
    assert response.status_code == 200
    products_response = ProductListResponse.model_validate(response.json())
    assert products_response.products.__len__() > 0
    assert products_response.skip == 0
    for product in products_response.products:
        assert (search_word in product.title.lower()) or (search_word in product.description.lower())


@pytest.mark.api
def test_get_products_by_category_with_limit(api_client):
    response = api_client.get('products/category-list')
    assert response.status_code == 200
    category_response = response.json()
    assert category_response.__len__() > 0

    categories = random.sample(category_response, 3)
    for category in categories:
        limit = 5
        response = api_client.get(f'products/category/{category}', params={'limit': limit})
        assert response.status_code == 200

        products_response = ProductListResponse.model_validate(response.json())
        assert products_response.products.__len__() > 0
        assert products_response.skip == 0
        assert products_response.limit <= limit
        for product in products_response.products:
            assert category == product.category

@pytest.mark.api
@allure.title("test_update_product_title (Known failure due to mocked response which returns only part of original Product model)")
def test_update_product_title(api_client):
    product_id = random.randint(1, 100)
    new_title = Faker().word()

    response = api_client.put(f'products/{product_id}', json={'title': new_title})
    assert response.status_code == 200
    print(response.json())
    product_response = ProductResponse.model_validate(response.json())
    assert product_response.title == new_title

@pytest.mark.api
def test_delete_product(api_client):
    product_id = random.randint(1, 100)
    response = api_client.delete(f'products/{product_id}')
    assert response.status_code == 200
    product_response = DeletedProductResponse.model_validate(response.json())


