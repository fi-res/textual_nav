from abc import abstractmethod
from typing import TYPE_CHECKING, Literal

from textual.app import ComposeResult
from textual.containers import Center, Vertical, Widget
from textual.geometry import Size
from textual.message import Message
from textual.widgets import Static

from textual_nav.page import NavPage

if TYPE_CHECKING:
    from textual_nav.app import NavApp


class Tab(Widget):
    DEFAULT_CSS = """
    Tab {
        padding: 1 2;
        height: auto;
    }
    Tab:hover {
        background: $surface-darken-1;
    }
    Tab.current {
        background: $surface-darken-2;
    }
    """
    app: "NavApp"

    class Clicked(Message):
        def __init__(self, tab_name: str):
            super().__init__()
            self.tab_name = tab_name

    def __init__(self, *children: Widget, name: str):
        super().__init__(*children)
        self.tab_name = name
        if self.app.current_tab == self.tab_name:
            self.add_class("current")

    def on_click(self):
        self.post_message(self.Clicked(self.tab_name))


class BaseNavigationWidget(Widget):
    app: "NavApp"

    def __init_subclass__(
        cls,
        layout: Literal["horizontal", "vertical"],
        width: Literal["auto"] | int = "auto"
    ):
        super().__init_subclass__()
        cls._layout = layout
        cls._width = width

    def __init__(self, pages: list[NavPage]):
        super().__init__()
        self.pages = pages
        self.styles.layout = self._layout
        if self._layout == "vertical":
            self.styles.height = "1fr"
            self.styles.width = self._width
        else:
            self.styles.height = "auto"
            self.styles.width = "1fr"

    @abstractmethod
    def compose_tab(self, name: str, icon: str | None = None) -> Widget: ...

    def compose(self) -> ComposeResult:
        for page in self.pages:
            assert page.tab_name, "Page should have tab_name to appear in navigation"
            yield Tab(
                self.compose_tab(page.tab_name, page.tab_icon), name=page.tab_name
            )


class NavigationRail(BaseNavigationWidget, layout="vertical", width=6):
    DEFAULT_CSS = """
    NavigationRail {
        padding: 0;
        background: $surface;
    }
    """

    def compose_tab(self, name: str, icon: str | None = None):
        assert icon is not None, "Tab icon is required for navigation rail"
        return Static(icon)


class NavigationDrawer(BaseNavigationWidget, layout="vertical", width="auto"):
    DEFAULT_CSS = """
    NavigationDrawer {
        padding: 1;
        background: $surface;
    }
    NavigationDrawer > Tab {
        margin-bottom: 1;
    }
    NavigationDrawer > Tab:last-child {
        margin-bottom: 0;
    }

    """

    def compose_tab(self, name: str, icon: str | None = None):
        return Static(f"{icon}  {name}" if icon else name)

    def get_content_width(self, container: Size, viewport: Size) -> int:
        return (
            max(
                (
                    len(page.tab_name or "") + (4 if page.tab_icon else 0)
                    for page in self.pages
                )
            )
            + 2
        )


# class NavigationBar(BaseNavigationWidget, layout="horizontal"):
#     DEFAULT_CSS = """
#     NavigationBar {
#         padding: 2;
#         background: $surface;
#     }
#     NavigationBar > Vertical {
#         width: auto;
#         height: auto;
#     }
#     NavigationBar Static {
#         width: auto;
#     }
#     # NavigationBar {
#     #     align: space-around; # why they still havent space between/around/evenly
#     # }
#     """

#     def compose_tab(self, name: str, icon: str | None = None):
#         if icon:
#             return Vertical(Static(icon), Static(name))
#         return Static(name)
