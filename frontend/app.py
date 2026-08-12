import sys

from pathlib import Path

from PySide6.QtWidgets import QApplication, QMainWindow

from backend.manager import Manager, get_project_directory
from backend.games.ut99 import UT99GameAdapter

from frontend.views.library import Library


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RedeeMOD")
        self.resize(960, 600)
        self.setMinimumSize(720, 480)
        self.setMaximumSize(1920, 1080)

        self.mod_manager = Manager()
        self.game_adapter = UT99GameAdapter()

        # Load Library View
        self.library_view = Library(self, self.mod_manager, self.game_adapter)
        self.setCentralWidget(self.library_view)


def load_stylesheet(app: QApplication):
    style_path = Path(get_project_directory()) / "frontend" / "styles" / "style.qss"

    if not style_path.exists():
        raise FileNotFoundError(f"Stylesheet missing at expected location: {style_path}")

    with open(style_path, "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    load_stylesheet(app)

    window = App()
    window.show()

    sys.exit(app.exec())
