from typing import Callable

from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QCheckBox, QPushButton, QWidget
from PySide6.QtCore import Qt

from frontend.components.card import Card


class ModCard(Card):
    """Mod item card."""

    def __init__(
        self,
        parent: QWidget,
        mod_name: str,
        is_selected: bool,
        on_toggle: Callable[[str, bool], None],
        on_delete: Callable[[str], None],
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

        banner_lbl = QLabel("MOD")
        banner_lbl.setObjectName("BannerLabel")
        banner_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        banner_layout.addWidget(banner_lbl)
        self.card_layout.addWidget(banner)

        lbl_title = QLabel(mod_name)
        lbl_title.setObjectName("CardTitleLabel")

        self.card_layout.addWidget(lbl_title)

        self.chk = QCheckBox("Enable mod")
        self.chk.setObjectName("CardCheckBox")
        self.chk.setChecked(is_selected)
        self.chk.toggled.connect(self._handle_toggle)
        self.card_layout.addWidget(self.chk)

        self.card_layout.addStretch()

        btn_delete = QPushButton("Remove mod")
        btn_delete.setObjectName("RemoveBtn")
        btn_delete.setFixedHeight(24)
        btn_delete.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_delete.clicked.connect(lambda: self.on_delete(self.mod_name))

        self.card_layout.addWidget(btn_delete)

        self._update_card_style()

    def _update_card_style(self):
        self.setProperty("selected", "true" if self.is_selected else "false")
        self.style().unpolish(self)
        self.style().polish(self)

    def _handle_toggle(self, checked: bool):
        self.is_selected = checked
        self._update_card_style()
        self.on_toggle(self.mod_name, checked)
