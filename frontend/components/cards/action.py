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

        plus_lbl = QLabel("+")
        plus_lbl.setObjectName("ActionPlusLabel")
        plus_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        banner_layout.addWidget(plus_lbl)
        self.card_layout.addWidget(banner)

        lbl_title = QLabel(title)
        lbl_title.setObjectName("CardTitleLabel")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.card_layout.addWidget(lbl_title)

        if subtitle:
            lbl_sub = QLabel(subtitle)
            lbl_sub.setObjectName("BannerLabel")
            lbl_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)

            self.card_layout.addWidget(lbl_sub)

        self.card_layout.addStretch()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()

        super().mousePressEvent(event)
