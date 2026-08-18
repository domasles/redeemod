from typing import Callable
from pathlib import Path

from PySide6.QtWidgets import QFrame, QVBoxLayout, QPushButton
from PySide6.QtCore import QObject, Qt, Signal
from PySide6.QtGui import QPixmap

from frontend.components.card import Card, BannerImageLabel
from frontend.components.elided_label import ElidedLabel


class GameCard(Card):
    """Game item card with fixed height alignment."""

    clicked = Signal()

    def __init__(
        self,
        parent: QObject,
        display_name: str,
        subtitle: str | None = None,
        on_delete: Callable[[], None] | None = None,
        logo: str | Path | QPixmap | None = None,
    ):
        super().__init__(parent)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.on_delete = on_delete

        banner = QFrame()
        banner.setObjectName("BannerFrame")
        banner.setFixedHeight(120)

        banner_layout = QVBoxLayout(banner)
        banner_layout.setContentsMargins(0, 0, 0, 0)

        banner_lbl = BannerImageLabel()
        banner_lbl.setObjectName("BannerLabel")
        banner_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        loaded_pixmap = None

        if logo:
            if isinstance(logo, QPixmap):
                loaded_pixmap = logo

            else:
                pixmap = QPixmap(str(logo))

                if not pixmap.isNull():
                    loaded_pixmap = pixmap

        if loaded_pixmap:
            banner_lbl.set_banner_pixmap(loaded_pixmap)

        else:
            banner_lbl.setText("GAME")

        banner_layout.addWidget(banner_lbl)
        self.card_layout.addWidget(banner)

        lbl_title = ElidedLabel(display_name)
        lbl_title.setObjectName("CardTitleLabel")

        self.card_layout.addWidget(lbl_title, alignment=Qt.AlignmentFlag.AlignCenter)

        if subtitle:
            lbl_sub = ElidedLabel(subtitle)
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
