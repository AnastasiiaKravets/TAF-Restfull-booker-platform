import random


def get_random_id(start = 1, end = 100):
    return random.randint(start, end)

def get_product_for_cart():
    return dict(id = get_random_id(),
                quantity = random.randint(1, 100))

def get_cart_payload(user_id = None, merge = None, number_of_products = 1):
    payload = dict(products = [])
    for _ in range(number_of_products):
        payload['products'].append(get_product_for_cart())
    if user_id:
        payload['userId'] = user_id
    if merge:
        payload['merge'] = merge
    return payload