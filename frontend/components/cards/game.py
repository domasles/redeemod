from typing import Callable, Optional

from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton, QWidget
from PySide6.QtCore import Qt, Signal

from frontend.components.card import Card


class GameCard(Card):
    """Game item card with fixed height alignment."""

    clicked = Signal()

    def __init__(self, parent: QWidget, display_name: str, subtitle: str = "", on_delete: Optional[Callable[[], None]] = None):
        super().__init__(parent)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.on_delete = on_delete

        banner = QFrame()
        banner.setObjectName("BannerFrame")
        banner.setFixedHeight(120)

        banner_layout = QVBoxLayout(banner)
        banner_layout.setContentsMargins(0, 0, 0, 0)

        banner_lbl = QLabel("GAME")
        banner_lbl.setObjectName("BannerLabel")

        banner_layout.addWidget(banner_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        self.card_layout.addWidget(banner)

        lbl_title = QLabel(display_name)
        lbl_title.setObjectName("CardTitleLabel")

        self.card_layout.addWidget(lbl_title, alignment=Qt.AlignmentFlag.AlignCenter)

        if subtitle:
            lbl_sub = QLabel(subtitle)
            lbl_sub.setObjectName("BannerLabel")

            self.card_layout.addWidget(lbl_sub, alignment=Qt.AlignmentFlag.AlignCenter)

        self.card_layout.addStretch()

        if self.on_delete:
            btn_delete = QPushButton("Remove game")
            btn_delete.setObjectName("RemoveBtn")
            btn_delete.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_delete.clicked.connect(self._handle_delete)

            self.card_layout.addWidget(btn_delete, alignment=Qt.AlignmentFlag.AlignCenter)

    def _handle_delete(self):
        if self.on_delete:
            self.on_delete()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            child = self.childAt(event.pos())

            if isinstance(child, QPushButton):
                return

            self.clicked.emit()

        super().mousePressEvent(event)
