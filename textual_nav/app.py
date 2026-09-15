from abc import abstractmethod
from typing import Literal

from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widget import Widget

from textual_nav.page import NavPage


class Nav(Widget):
    DEFAULT_CSS = """
    Nav {
        height: 100vh;
        width: auto;
    }
    """

    def __init__(
        self,
        *children: Widget,
        dock: Literal["left", "right", "top", "bottom"] = "left"
    ):
        super().__init__(*children)
        self.styles.dock = dock


class NavApp(App):
    NAV_POSITION: Literal["left", "right", "top", "bottom"] = "left"
    PAGES: list[NavPage]
    DEFAULT_PAGE: NavPage | None = None
    _pages_stack: reactive[list[NavPage]] = reactive([], recompose=True)
    _page: NavPage
    nav_visible: reactive[bool] = reactive(True, recompose=True)

    def __init__(self):
        super().__init__()

        if not self.DEFAULT_PAGE:
            self.DEFAULT_PAGE = self.PAGES[0]
        self.push_screen(self.DEFAULT_PAGE)

    @abstractmethod
    def compose_nav(self) -> ComposeResult: ...

    def push_screen(self, page: NavPage):  # ty: ignore
        self._pages_stack = [*self._pages_stack, page]  # append dont trigger reactive

    def switch_screen(self, page: NavPage):  # ty: ignore
        self._page = page
        self._pages_stack = [page]

    def pop_screen(self):
        assert len(self._pages_stack) > 1, "No pages to pop"
        self._pages_stack = self._pages_stack[:-1]

    def compose(self):
        if self.nav_visible:
            yield Nav(*self.compose_nav(), dock=self.NAV_POSITION)
        yield self._pages_stack[-1]
