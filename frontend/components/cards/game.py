from collections.abc import Callable
from pathlib import Path

from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QWidget
from PySide6.QtCore import Qt, Signal

from frontend.components.images.banner import BannerImage
from frontend.components.elided_label import ElidedLabel
from frontend.components.card import Card


class GameCard(Card):
    """Game item card with fixed height alignment."""

    clicked = Signal()

    def __init__(
        self,
        parent: QWidget,
        display_name: str,
        subtitle: str | None = None,
        on_delete: Callable[[], None] | None = None,
        on_settings: Callable[[], None] | None = None,
        logo: str | Path | None = None,
    ):
        super().__init__(parent)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.on_delete = on_delete
        self.on_settings = on_settings

        banner = QFrame()
        banner.setObjectName("BannerFrame")
        banner.setFixedHeight(120)

        banner_layout = QVBoxLayout(banner)
        banner_layout.setContentsMargins(0, 0, 0, 0)

        banner_lbl = BannerImage(logo)
        banner_lbl.setObjectName("BannerLabel")
        banner_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if not logo or not Path(logo).is_file():
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

        if self.on_settings or self.on_delete:
            button_layout = QHBoxLayout()
            button_layout.setContentsMargins(0, 0, 0, 0)
            button_layout.setSpacing(4)

            if self.on_settings:
                btn_settings = QPushButton("Settings")
                btn_settings.setObjectName("SettingsBtn")
                btn_settings.setCursor(Qt.CursorShape.PointingHandCursor)
                btn_settings.clicked.connect(self._handle_settings)

                button_layout.addWidget(btn_settings)

            if self.on_delete:
                btn_delete = QPushButton("Remove game")
                btn_delete.setObjectName("RemoveBtn")
                btn_delete.setCursor(Qt.CursorShape.PointingHandCursor)
                btn_delete.clicked.connect(self._handle_delete)

                button_layout.addWidget(btn_delete)

            self.card_layout.addLayout(button_layout)

    def _handle_delete(self):
        if self.on_delete:
            self.on_delete()

    def _handle_settings(self):
        if self.on_settings:
            self.on_settings()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            child = self.childAt(event.pos())

            if isinstance(child, QPushButton):
                return

            self.clicked.emit()

        super().mousePressEvent(event)
