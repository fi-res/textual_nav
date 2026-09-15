from typing import TYPE_CHECKING

from textual.widget import Widget

if TYPE_CHECKING:
    from textual_nav.app import NavApp


class NavPage(Widget):
    app: "NavApp"

    def __init_subclass__(cls, name: str):
        super().__init_subclass__()
        cls.name = name

    def pop(self):
        self.app.pop_screen()

    def push(self, page: "NavPage"):
        self.app.push_screen(page)

    def switch(self, page: "NavPage"):
        self.app.switch_screen(page)
