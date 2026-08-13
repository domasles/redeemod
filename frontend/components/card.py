from typing import Optional

from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget
from PySide6.QtCore import Qt


class Card(QFrame):
    """Base composable Card container."""

    CARD_WIDTH = 200
    CARD_HEIGHT = 240

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.setFixedSize(self.CARD_WIDTH, self.CARD_HEIGHT)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.card_layout = QVBoxLayout(self)
        self.card_layout.setContentsMargins(12, 12, 12, 12)
        self.card_layout.setSpacing(12)
