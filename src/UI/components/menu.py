from src.UI.base_actions import BaseActions


class Menu(BaseActions):

    def __init__(self, page):
        super().__init__(page)

        self.main_content = page.locator('div.burger-container')
        self.aboutLink = page.locator('a.burger-text[href="/about"]')
        self.ownImportIcon = page.locator('i[data-autotestid="ecomui-icon-own-import"]')
