from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import QObject, Qt, Signal

from backend.manager import Manager
from backend.constants import *


class Sidebar(QWidget):
    navigated = Signal(str)

    def __init__(self, parent: QObject, manager: Manager):
        super().__init__(parent)

        self.manager = manager

        self.setObjectName("SidebarWidget")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setFixedWidth(180)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(10)

        title = QLabel(APP_NAME)
        title.setObjectName("LibraryTitle")

        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(15)

        btn_games = QPushButton("Games")
        btn_games.setObjectName("AddFolderBtn")
        btn_games.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_games.clicked.connect(lambda: self.navigated.emit("games"))

        layout.addWidget(btn_games)

        self.btn_library = QPushButton("Library")
        self.btn_library.setObjectName("AddFolderBtn")
        self.btn_library.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_library.clicked.connect(lambda: self.navigated.emit("library"))

        layout.addWidget(self.btn_library)
        layout.addStretch()

        self.refresh_visibility()

    def refresh_visibility(self):
        """Checks whether the Library button should be visible."""

        has_games = bool(self.manager.get_added_games())
        self.btn_library.setVisible(has_games)
