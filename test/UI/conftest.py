import pytest
from playwright.sync_api import sync_playwright

from src.UI.utils.playwright_manager import PlaywrightManager


@pytest.fixture(scope="session", autouse=True)
def playwright():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session", autouse=True)
def browser(playwright):
    manager = PlaywrightManager(playwright)
    browser = manager.create_browser()
    yield browser

    browser.close()


@pytest.fixture(scope='function')
def page(browser, playwright):
    manager = PlaywrightManager(playwright)
    context = manager.create_context(browser)
    page = context.new_page()
    yield page

    context.close()

# @pytest.fixture(scope="function", autouse=True)
# def open_page(page, browser_context):
#     print("open page fixture opening")
#
#     page.goto("/")
#     cookies = {
#       "name": "agreeUseCookies",
#       "value": "1776851443983",
#       "domain": ".silpo.ua",
#       "path": "/",
#       "expires": 1810546875,
#       "httpOnly": False,
#       "secure": False,
#       "sameSite": "Lax"
#     }
#     browser_context.add_cookies([cookies])
#
# @pytest.fixture(scope="function")
# def authorized(page, browser_context):
#     print("authorized fixture opening")
#
#     token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjA2RkNFODI2RTc2NUZGMEFBQjAwODQ3QTk2Q0MwMDE0RDQ4NkJDNUNSUzI1NiIsInR5cCI6ImF0K2p3dCIsIng1dCI6IkJ2em9KdWRsX3dxckFJUjZsc3dBRk5TR3ZGdyJ9.eyJuYmYiOjE3NzY4NTE5MTQsImV4cCI6MTc3NjkzODMxNCwiaXNzIjoiaHR0cHM6Ly9hdXRoLnNpbHBvLnVhIiwiY2xpZW50X2lkIjoic2lscG8tLXNpdGUtLXNwYSIsInN1YiI6IjFlZDAwMjAwLTMyYzAtNjAwOC1hNjVmLTg3MTA5MjZiYTgzZiIsImF1dGhfdGltZSI6MTc3Njg1MTkwOSwiaWRwIjoib3RwIiwic2Vzc2lvbklkIjoiNzFiYTU3NDQtMmFjMy00MTY0LTg1MGYtMjFjNjE2OGFjNzJjIiwianRpIjoiOTdFODM3NEE3MzEyN0MzQTIwQzhGRDBCMDkzN0IzMkMiLCJpYXQiOjE3NzY4NTE5MTQsInNjb3BlIjpbInB1YmxpYy1teSIsIm9wZW5pZCJdfQ.Bkqo0h_9f1bDIbZNjt3uMEgMHug-_7mchRl5TsEJn4hCgpyG9YF28nVKvA9I4UMQLWI_KrFMj0uU-UdkA2BjpOxCXeXaBxZZ4wOXuHAEfUr8MkHDjydxIwfGo4P3r-NSPHWPxPx3v_hgTXC2Rym_BHnauWP0PtHwqfRpDzdi17qdaC9MsffDikjLQ4RtCsjej4hFM_dLtfQ9qR7NGuzl6OtZ7fdZi_UZPpy2hF77KKARZYMxgnN9Wn99EZR6Vi9xtiUvPR8PcVNixQP5PGXii6McZk7v-2-3aYwTiySWMDFlZl2zT4bPhQ_c_mkTDmBHJJH8atv1-hF9sewFNTnVtw"
#     page.evaluate(f"localStorage.setItem('access_token', '{token}')")
