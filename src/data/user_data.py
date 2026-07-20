from config import settings


def get_valid_user():
    return {'username': settings.RESTFULL_USER, 'password': settings.RESTFULL_PASSWORD}