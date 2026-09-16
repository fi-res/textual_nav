from typing import TYPE_CHECKING

from textual.widget import Widget

if TYPE_CHECKING:
    from textual_nav.app import NavApp


class NavPage(Widget):
    app: "NavApp"

    def __init_subclass__(
        cls, tab_name: str | None = None, tab_icon: str | None = None
    ):
        super().__init_subclass__()
        cls.tab_name = tab_name
        cls.tab_icon = tab_icon

    def pop(self):
        self.app.pop_page()

    def push(self, page: "NavPage | str"):
        self.app.push_page(page)

    def switch(self, page: "NavPage | str"):
        self.app.switch_page(page)
