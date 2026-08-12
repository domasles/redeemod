from typing import Callable

from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QCheckBox, QPushButton
from PySide6.QtCore import Qt


class Card(QFrame):
    def __init__(
        self,
        parent,
        mod_name: str,
        is_selected: bool,
        on_toggle: Callable[[str, bool], None],
        on_delete: Callable[[str], None],
    ):
        super().__init__(parent)
        self.setFixedSize(200, 220)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.mod_name = mod_name
        self.is_selected = is_selected
        self.on_toggle = on_toggle
        self.on_delete = on_delete

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(6)

        # Thumbnail Banner Area
        banner = QFrame()
        banner.setObjectName("BannerFrame")
        banner.setFixedHeight(110)
        banner_layout = QVBoxLayout(banner)
        banner_layout.setContentsMargins(0, 0, 0, 0)

        banner_lbl = QLabel("MOD BANNER")
        banner_lbl.setObjectName("BannerLabel")
        banner_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        banner_layout.addWidget(banner_lbl)

        layout.addWidget(banner)

        # Title Label
        lbl_title = QLabel(mod_name)
        lbl_title.setObjectName("CardTitleLabel")

        layout.addWidget(lbl_title)

        # Checkbox for multi-selection
        self.chk = QCheckBox("Enable Mod")
        self.chk.setObjectName("CardCheckBox")
        self.chk.setChecked(is_selected)
        self.chk.toggled.connect(self._handle_toggle)

        layout.addWidget(self.chk)

        # Delete Button
        btn_delete = QPushButton("Remove")
        btn_delete.setObjectName("RemoveBtn")
        btn_delete.setFixedHeight(24)
        btn_delete.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_delete.clicked.connect(lambda: self.on_delete(self.mod_name))

        layout.addWidget(btn_delete)
        self._update_card_style()

    def _update_card_style(self):
        self.setProperty("selected", "true" if self.is_selected else "false")
        self.style().unpolish(self)
        self.style().polish(self)

    def _handle_toggle(self, checked: bool):
        self.is_selected = checked
        self._update_card_style()
        self.on_toggle(self.mod_name, checked)
