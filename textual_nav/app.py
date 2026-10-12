from typing import Literal, cast

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static

from textual_nav.page import NavPage
from textual_nav.widgets import BaseNavigationWidget, NavTab


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
    NO_CONTENT_NOTICE: bool = True
    _pages_stack: list[NavPage] = []
    nav_visible: reactive[bool] = reactive(True, init=False)
    page_visible: reactive[bool] = reactive(True, init=False)
    current_tab: reactive[str] = reactive("")

    def on_mount(self):
        self.switch_page(self.DEFAULT_PAGE or self.PAGES[0])

    def compose_nav(self) -> ComposeResult:
        assert self.NAV_TYPE, "set NAV_TYPE or override compose_nav"
        yield self.NAV_TYPE(self.PAGES)

    def push_page(self, page: NavPage | type[NavPage] | str, *args, **kwargs):
        """Push new subpage (current page still will be highlighted)"""
        page = self._resolve_page(page, *args, **kwargs)
        self._set_stack([*self._pages_stack, page])

    def switch_page(self, page: NavPage | type[NavPage] | str, *args, **kwargs):
        """Switch to another page. New page will be highlighted. New page should exist in self.PAGES"""
        page = self._resolve_page(page, *args, **kwargs)
        assert page.tab_name, "Page should have name"
        self._set_stack([page])
        self.current_tab = page.tab_name

    def pop_page(self):
        """Pop current subpage (from push_page)."""
        assert len(self._pages_stack) > 1, "No pages to pop"
        self._set_stack(self._pages_stack[:-1])

    def _resolve_page(
        self, page: NavPage | type[NavPage] | str, *args, **kwargs
    ) -> NavPage:
        """Return a mounted page instance, reusing cached ones when possible."""
        container = self.query_one("#pages", Container)

        if isinstance(page, str):
            found = next((p for p in self.PAGES if p.tab_name == page), None)
            if found is None:
                raise RuntimeError(f"Page {page!r} not found")
            page = found

        if isinstance(page, NavPage):
            instance = page
            instance._disposable = not page.CAN_CACHE
        else:
            # Pages created with arguments are usually one-off (e.g. a post by id)
            disposable = bool(args or kwargs) or not page.CAN_CACHE
            if not disposable:
                instance = next(
                    (
                        p
                        for p in container.children
                        if type(p) is page and not cast(NavPage, p)._disposable
                    ),
                    None
                )
            else:
                instance = None
            if instance is None:
                instance = page(*args, **kwargs)
                instance._disposable = disposable

        if instance.parent is None:
            instance.display = False
            container.mount(instance)
        return cast(NavPage, instance)

    def _set_stack(self, stack: list[NavPage]):
        # Disposable pages are destroyed once they leave the stack
        for page in self._pages_stack:
            if page not in stack and page._disposable:
                page.remove()
        self._pages_stack = stack

        top = stack[-1] if stack else None
        for child in self.query_one("#pages", Container).children:
            child.display = child is top
        if top is None:
            self.query_one("#no-content").display = self.NO_CONTENT_NOTICE

    def watch_current_tab(self):
        self.query(BaseNavigationWidget).refresh(recompose=True)

    def watch_nav_visible(self, visible: bool):
        self.query_one(Nav).display = visible

    def watch_page_visible(self, visible: bool):
        self.query_one("#pages").display = visible

    def compose(self) -> ComposeResult:
        nav = Nav(*self.compose_nav(), dock=self.NAV_POSITION)
        nav.display = self.nav_visible
        yield nav

        pages = Container(id="pages")
        pages.display = self.page_visible
        with pages:
            yield Static("[no content]", id="no-content")

    def on_nav_tab_clicked(self, event: NavTab.Clicked):
        event.stop()
        self.switch_page(event.tab_name)
