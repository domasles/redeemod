from typing import Callable
from pathlib import Path

from PySide6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from frontend.components.card import Card, BannerImageLabel
from frontend.components.elided_label import ElidedLabel


class ModCard(Card):
    """Mod item card."""

    def __init__(
        self,
        parent: QWidget,
        mod_name: str,
        is_selected: bool,
        on_toggle: Callable[[str, bool], None],
        on_delete: Callable[[str], None],
        logo: str | Path | QPixmap | None = None,
    ):
        super().__init__(parent)

        self.mod_name = mod_name
        self.is_selected = is_selected
        self.on_toggle = on_toggle
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
            banner_lbl.setText("MOD")

        banner_layout.addWidget(banner_lbl)
        self.card_layout.addWidget(banner)

        lbl_title = ElidedLabel(mod_name)
        lbl_title.setObjectName("CardTitleLabel")

        self.card_layout.addWidget(lbl_title, alignment=Qt.AlignmentFlag.AlignCenter)

        self.btn_enable = QPushButton("Enable mod")
        self.btn_enable.setObjectName("LaunchBtn")
        self.btn_enable.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_enable.setCheckable(True)
        self.btn_enable.setChecked(is_selected)
        self.btn_enable.toggled.connect(self._handle_toggle)

        self.card_layout.addWidget(self.btn_enable, alignment=Qt.AlignmentFlag.AlignCenter)
        self.card_layout.addStretch()

        btn_delete = QPushButton("Remove mod")
        btn_delete.setObjectName("RemoveBtn")
        btn_delete.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_delete.clicked.connect(lambda: self.on_delete(self.mod_name))

        self.card_layout.addWidget(btn_delete, alignment=Qt.AlignmentFlag.AlignCenter)

        self._update_card_style()
        self._update_enable_button_text()

    def _update_card_style(self):
        self.setProperty("selected", "true" if self.is_selected else "false")

        self.style().unpolish(self)
        self.style().polish(self)

    def _update_enable_button_text(self):
        if self.is_selected:
            self.btn_enable.setText("Disable mod")

        else:
            self.btn_enable.setText("Enable mod")

    def _handle_toggle(self, checked: bool):
        self.is_selected = checked

        self._update_card_style()
        self._update_enable_button_text()

        self.on_toggle(self.mod_name, checked)
