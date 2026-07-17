from UI.admin_part.components.header import HeaderComponent
from UI.common.base_page import BasePage


class RoomPage(BasePage):
    url_part = 'admin/rooms'

    def __init__(self, page):
        super().__init__(page)
        self.header = HeaderComponent(page)
