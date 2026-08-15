from typing import Optional

from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QWidget
from PySide6.QtCore import Qt, Signal

from frontend.components.card import Card


class ActionCard(Card):
    """Action Card for adding games or mods."""

    clicked = Signal()

    def __init__(self, parent: Optional[QWidget], title: str, subtitle: str = ""):
        super().__init__(parent)

        self.setObjectName("ActionCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        banner = QFrame()
        banner.setObjectName("BannerFrame")
        banner.setFixedHeight(120)

        banner_layout = QVBoxLayout(banner)
        banner_layout.setContentsMargins(0, 0, 0, 0)

        banner_lbl = QLabel("+")
        banner_lbl.setObjectName("ActionPlusLabel")

        banner_layout.addWidget(banner_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        self.card_layout.addWidget(banner)

        lbl_title = QLabel(title)
        lbl_title.setObjectName("CardTitleLabel")

        self.card_layout.addWidget(lbl_title, alignment=Qt.AlignmentFlag.AlignCenter)

        if subtitle:
            lbl_sub = QLabel(subtitle)
            lbl_sub.setObjectName("BannerLabel")

            self.card_layout.addWidget(lbl_sub, alignment=Qt.AlignmentFlag.AlignCenter)

        self.card_layout.addStretch()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()

        super().mousePressEvent(event)
