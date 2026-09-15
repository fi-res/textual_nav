from textual.widgets import Button, Static

from textual_nav import NavApp, NavPage


class Page1(NavPage, name="page-1"):
    def compose(self):
        yield Static("page 1")


class Page2(NavPage, name="page-2"):
    def compose(self):
        yield Static("page 2")


class Page3(NavPage, name="page-3"):
    def compose(self):
        yield Static("page 3")
        yield Button("go page 2")

    def on_button_pressed(self):
        self.switch(Page2())


class Page4(NavPage, name="page-4"):
    def compose(self):
        yield Static("page 4")
        yield Button("go page 5")

    def on_button_pressed(self):
        self.push(Page5())


class Page5(NavPage, name="page-5"):
    def compose(self):
        yield Static("page 5")
        yield Button("go back")

    def on_button_pressed(self):
        self.pop()


class ExampleApp(NavApp):
    DEFAULT_PAGE = Page1()

    def compose_nav(self):
        yield Button("page-1", id="page-1")
        yield Button("page-2", id="page-2")
        yield Button("page-3", id="page-3")
        yield Button("page-4", id="page-4")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "page-1":
            self.switch_screen(Page1())
        if event.button.id == "page-2":
            self.switch_screen(Page2())
        if event.button.id == "page-3":
            self.switch_screen(Page3())
        if event.button.id == "page-4":
            self.switch_screen(Page4())


ExampleApp().run()
