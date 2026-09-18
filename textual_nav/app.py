from typing import Literal

from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widget import Widget

from textual_nav.page import NavPage
from textual_nav.widgets import BaseNavigationWidget, Tab


class Nav(Widget):
    DEFAULT_CSS = """
    Nav {
        height: auto;
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
    PAGES: list[NavPage | type[NavPage]]
    NAV_TYPE: type[BaseNavigationWidget] | None = None
    DEFAULT_PAGE: NavPage | None = None
    _pages_stack: reactive[list[NavPage]] = reactive([], recompose=True)
    _page: NavPage
    _pages_cache: list[NavPage] = []
    nav_visible: reactive[bool] = reactive(True, recompose=True)
    current_tab: reactive[str] = reactive("", recompose=True)

    def on_mount(self):
        self.switch_page(self.DEFAULT_PAGE or self.PAGES[0])

    def compose_nav(self) -> ComposeResult:
        assert self.NAV_TYPE, "set NAV_TYPE or override compose_nav"
        yield self.NAV_TYPE(self.PAGES)

    def push_page(self, page: NavPage | type[NavPage] | str, *args, **kwargs):
        """Push new subpage (current page still will be highlighted)"""
        page = self._resolve_page(page, *args, **kwargs)
        self._pages_stack = [*self._pages_stack, page]  # append dont trigger reactive

    def switch_page(self, page: NavPage | type[NavPage] | str, *args, **kwargs):
        """Switch to another page. New page will be highlighted. New page should exists in self.PAGES"""
        page: NavPage = self._resolve_page(page, *args, **kwargs)
        assert page.tab_name, "Page should have name"
        self._page = page
        self._pages_stack = [page]
        self.current_tab = page.tab_name

    def pop_page(self):
        """Pop current subpage (from push_screen)."""
        assert len(self._pages_stack) > 1, "No pages to pop"
        self._pages_stack = self._pages_stack[:-1]  # pop dont trigger reactive

    def _resolve_page(self, page: NavPage | type[NavPage] | str, *args, **kwargs):
        if isinstance(page, NavPage):
            return page

        if cached_page := next(
            (p for p in self._pages_cache if p.tab_name == page or p is page), None
        ):
            return cached_page
        if isinstance(page, str):
            if instance := next((p for p in self.PAGES if p.tab_name == page), None):
                instance = (
                    instance
                    if isinstance(instance, NavPage)
                    else instance(*args, **kwargs)
                )
                self._pages_cache.append(instance)
                return instance
            raise RuntimeError(f"Page {page!r} not found")

        instance = page if isinstance(page, NavPage) else page(*args, **kwargs)
        self._pages_cache.append(instance)
        return instance

    def compose(self):
        if self.nav_visible:
            yield Nav(*self.compose_nav(), dock=self.NAV_POSITION)
        if self._pages_stack:
            yield self._pages_stack[-1]

    def on_tab_clicked(self, event: Tab.Clicked):
        event.stop()
        self.switch_page(event.tab_name)
