# textual_nav

Add navigation bars to your textual app easily.

## Example
```py
from textual.widgets import Static, Button
from textual_nav import NavApp, NavPage

class Page1(NavPage, name='page-1'):
    def compose(self):
        yield Static('page #1')

class Page2(NavPage, name='page-2'):
    def compose(self):
        yield Static('page #2')

class MyApp(NavApp):
    def compose_nav(self):
        yield Button('page 1', id='page1')
        yield Button('page 2', id='page2')

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "page-1":
            self.switch_screen(Page1())
        if event.button.id == "page-2":
            self.switch_screen(Page2())
```


## API

### NavApp
Base app class.

#### Attributes
 - `NAV_POSITION` (literal `left` | `right` | `top` | `bottom`): Position for navigation bar. Defaults to `left`.
 - `DEFAULT_PAGE` (instance of `NavPage`): Default page to be opened on app startup. Required.
 - `nav_visible` (reactive - bool): Is navigation bar visible. Defaults to `true`.

#### Methods
 - `compose_nav`: Compose navigation bar. Required to override.
 - `push_screen`: Push new screen on top of current stack.
 - `pop_screen`: Pop most top screen in the stack. If there is only one page in the stack, exception will be throwen.
 - `switch_screen`: Switch current screen to another one.

 > [!NOTE]
 > Please do not override `compose` method. Content will be composed from `compose_nav` and the most top page in the stack.

### NavPage
Base page class.

#### Methods
 - `pop` / `push` / `switch`: Aliases for app's `pop_screen`, `push_screen` and `switch_screen`.
