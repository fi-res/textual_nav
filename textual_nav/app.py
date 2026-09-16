from typing import Literal

from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widget import Widget

from textual_nav.page import NavPage
from textual_nav.widgets import BaseNavigationWidget, Tab


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
    NAV_TYPE: type[BaseNavigationWidget] | None = None
    DEFAULT_PAGE: NavPage | None = None
    _pages_stack: reactive[list[NavPage]] = reactive([], recompose=True)
    _page: NavPage
    nav_visible: reactive[bool] = reactive(True, recompose=True)
    current_tab: str

    def __init__(self):
        super().__init__()
        self.switch_page(self.DEFAULT_PAGE or self.PAGES[0], _initital=True)

    def compose_nav(self) -> ComposeResult:
        assert self.NAV_TYPE, "set NAV_TYPE or override compose_nav"
        yield self.NAV_TYPE(self.PAGES)

    def push_page(self, page: NavPage | str):
        """Push new subpage (current page still will be highlighted)"""
        page = self._resolve_page(page)
        self._pages_stack = [*self._pages_stack, page]  # append dont trigger reactive

    def switch_page(self, page: NavPage | str, _initital: bool = False):
        """Switch to another page. New page will be highlighted. New page should exists in self.PAGES"""
        page: NavPage = self._resolve_page(page)
        assert page.tab_name, "Page should have name"
        self._page = page
        self._pages_stack = [page]
        if not _initital:
            self._get_current_tab().remove_class("current")  # unset prev tab
        self.current_tab = page.tab_name
        self.call_after_refresh(
            lambda: self._get_current_tab().add_class("current")
        )  # set current tab

    def pop_page(self):
        """Pop current subpage (from push_screen)."""
        assert len(self._pages_stack) > 1, "No pages to pop"
        self._pages_stack = self._pages_stack[:-1]  # pop dont trigger reactive

    def _resolve_page(self, page: NavPage | str):
        if isinstance(page, str):
            _page = next((p for p in self.PAGES if p.tab_name == page), None)
            if _page is None:
                raise RuntimeError(f"Page {page!r} not found")
            return _page
        return page

    def _get_current_tab(self) -> Tab:
        return next(
            tab
            for tab in self.query_one(Nav).query(Tab)
            if tab.tab_name == self.current_tab
        )

    def compose(self):
        if self.nav_visible:
            yield Nav(*self.compose_nav(), dock=self.NAV_POSITION)
        yield self._pages_stack[-1]

    def on_tab_clicked(self, event: Tab.Clicked):
        event.stop()
        self.switch_page(event.tab_name)
