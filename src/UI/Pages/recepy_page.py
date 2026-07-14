from src.UI.base_page import BasePage


class RecepyPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.title = page.locator('h1[data-autotestid="recipes-catalog-title"]')
        self.hvLabel1_15 = page.locator('label[data-autotestid="recipes-filter-checkbox-115-xv"]')
