from playwright.sync_api import Page

from src.UI.components.header import Header
from src.UI.components.menu import Menu


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.header = Header(page)
        self.menu = Menu(page)
        # self.db = DataBase()
