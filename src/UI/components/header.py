from src.UI.base_actions import BaseActions


class Header(BaseActions):

    def __init__(self, page):
        super().__init__(page)

        self.searchField = page.get_by_role("searchbox", name="Я шукаю")
        self.suggestionContainer = page.locator("div[data-autotestid='silpo-search-suggest-list']")
        self.suggestedCategoryList = page.locator("silpo-search-suggested-category-list")
        self.suggestedCategoryListItems = page.locator("li.suggested-category-list-item")
        self.mainMenuButton = page.get_by_role("button", name="Відкрити головне меню")
        self.logo = page.get_by_role("link", name="Header logo")
        self.new = page.locator('1')

    def search_for(self, value):
        self.searchField.click()
        self.searchField.fill(value)

    def confirm_search(self):
        self.searchField.press("Enter")
