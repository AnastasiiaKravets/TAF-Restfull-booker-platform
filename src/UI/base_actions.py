from playwright.sync_api import Page


class BaseActions:
    def __init__(self, page: Page):
        self.page = page

    def click_first_visible(self, locator_str):
        visible_element = None
        locator = self.page.locator(locator_str)
        for i in range(locator.count()):
            el = locator.nth(i)
            if el.is_visible():
                visible_element = el
                break

        if visible_element:
            visible_element.click()
        else:
            raise BaseException("There is no visible elements")
