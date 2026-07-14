from src.UI.Pages.recepy_page import RecepyPage
from src.UI.base_page import BasePage


class MainPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.recepyLink = page.locator('a[href="/recipes"][data-autotestid="home-banners-tile_3"]')

    def open_recepy(self):
        self.recepyLink.click()
        return RecepyPage(self.page)
