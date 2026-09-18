from textual.widgets import Button, Static

from textual_nav import NavApp, NavPage
from textual_nav.widgets import NavigationDrawer


class Page1(NavPage, tab_name="Page 1", tab_icon="󰑹"):
    def compose(self):
        yield Static("page 1")


class Page2(NavPage, tab_name="Page 2", tab_icon=""):
    def compose(self):
        yield Static("page 2")
        yield Button("go page 6 (with number 1)", id="p1")
        yield Button("go page 6 (with number 2)", id="p2")
        yield Button("go page 6 (with number 3)", id="p3")

    def on_button_pressed(self, event: Button.Pressed):
        self.push(Page6, int(event.button.id.removeprefix("p")))


class Page3(NavPage, tab_name="Page 3", tab_icon=""):
    def compose(self):
        yield Static("page 3")
        yield Button("go page 2")

    def on_button_pressed(self):
        self.switch(Page2())


class Page4(NavPage, tab_name="Page 4", tab_icon=""):
    def compose(self):
        yield Static("page 4")
        yield Button("go page 5")

    def on_button_pressed(self):
        self.push(Page5())


class Page5(NavPage, tab_name="Page 5"):
    def compose(self):
        yield Static("page 5")
        yield Button("go back")

    def on_button_pressed(self):
        self.pop()


class Page6(NavPage, tab_name="Page 6"):
    def __init__(self, number: int):
        super().__init__()
        self.number = number

    def compose(self):
        yield Static("page 6")
        yield Static(f"Number: {self.number}")
        yield Button("go back")

    def on_button_pressed(self):
        self.pop()


class ExampleApp(NavApp):
    PAGES = [Page1, Page2, Page3, Page4]
    NAV_TYPE = NavigationDrawer
    NAV_POSITION = "left"
    CSS = """
    NavPage {
        padding: 1;
    }
    """


ExampleApp().run()
