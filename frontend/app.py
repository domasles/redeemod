import sys
import os

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from PySide6.QtGui import QIcon

from backend.utils.filesystem import get_project_directory
from backend.games import get_adapter_classes
from backend.manager import Manager
from backend.constants import *

from frontend.components.sidebar import Sidebar
from frontend.views.library import Library
from frontend.views.games import Games


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_NAME)
        self.resize(960, 600)
        self.setMinimumSize(960, 600)

        self.manager = Manager()
        self.adapters = {}

        for game_id, adapter_class in get_adapter_classes().items():
            try:
                adapter = adapter_class()
                self.adapters[game_id] = adapter

            except Exception:
                continue

        central_widget = QWidget()

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = Sidebar(self, self.manager)
        self.sidebar.navigated.connect(self._navigate_screen)
        self.manager.games_changed.connect(self.sidebar.refresh_library_visibility)

        main_layout.addWidget(self.sidebar)

        self.screen_stack = QStackedWidget()
        self.library_view = Library(self, self.manager, self.adapters)
        self.games_view = Games(self, self.manager, self.adapters)

        self.screen_stack.addWidget(self.library_view)
        self.screen_stack.addWidget(self.games_view)

        main_layout.addWidget(self.screen_stack)

        self.setCentralWidget(central_widget)

        self.games_view.refresh_games()
        self.screen_stack.setCurrentWidget(self.games_view)
        self.sidebar.refresh_library_visibility()

    def _navigate_screen(self, screen_name: str):
        self.sidebar.refresh_library_visibility()

        if screen_name == "library":
            if not self.manager.get_added_games():
                self.screen_stack.setCurrentWidget(self.games_view)
                return

            self.library_view.reset_state()
            self.screen_stack.setCurrentWidget(self.library_view)

        elif screen_name == "games":
            self.games_view.refresh_games()
            self.screen_stack.setCurrentWidget(self.games_view)


def load_stylesheet(app: QApplication):
    style_path = get_project_directory() / "frontend" / "styles" / "style.qss"

    if not style_path.exists():
        raise FileNotFoundError(f"Stylesheet missing at expected location: {style_path}")

    with open(style_path, "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())


def main():
    os.environ["QT_LOGGING_RULES"] = "qt.qpa.wayland.textinput=false"

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(str(APP_ICON_FILE_PATH)))

    load_stylesheet(app)

    window = App()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
