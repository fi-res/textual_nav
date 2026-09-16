from textual.widgets import Button, Static

from textual_nav import NavApp, NavPage
from textual_nav.widgets import NavigationBar, NavigationDrawer, NavigationRail


class Page1(NavPage, tab_name="Page 1", tab_icon="󰑹"):
    def compose(self):
        yield Static("page 1")


class Page2(NavPage, tab_name="Page 2", tab_icon=""):
    def compose(self):
        yield Static("page 2")


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


class ExampleApp(NavApp):
    PAGES = [Page1(), Page2(), Page3(), Page4()]
    NAV_TYPE = NavigationBar
    NAV_POSITION = "bottom"
    CSS = """
    NavPage {
        padding: 1;
    }
    """

    # def compose_nav(self):
    #     yield Button("page-1", id="page-1")
    #     yield Button("page-2", id="page-2")
    #     yield Button("page-3", id="page-3")
    #     yield Button("page-4", id="page-4")

    # def on_button_pressed(self, event: Button.Pressed):
    #     if event.button.id == "page-1":
    #         self.switch_screen(Page1())
    #     if event.button.id == "page-2":
    #         self.switch_screen(Page2())
    #     if event.button.id == "page-3":
    #         self.switch_screen(Page3())
    #     if event.button.id == "page-4":
    #         self.switch_screen(Page4())


ExampleApp().run()
