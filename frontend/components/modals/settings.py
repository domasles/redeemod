import shlex

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Signal, Qt


class SettingsModalBody(QWidget):
    options_saved = Signal(list)
    options_cancelled = Signal()

    def __init__(self, game_id: str, options: list[str]):
        super().__init__()

        self.setObjectName("SettingsModalBody")
        self.game_id = game_id
        self.options = list(options)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        info_label = QLabel("Extra launch options:")
        info_label.setObjectName("CardTitleLabel")
        info_label.setWordWrap(True)

        layout.addWidget(info_label)

        self.extra_options_edit = QLineEdit()
        self.extra_options_edit.setObjectName("DropdownTrigger")
        self.extra_options_edit.setText(" ".join(self.options))

        layout.addWidget(self.extra_options_edit)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)

        self.btn_save = QPushButton("Done")
        self.btn_save.setObjectName("LaunchBtn")
        self.btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_save.clicked.connect(self._on_save)

        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setObjectName("RemoveBtn")
        self.btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cancel.clicked.connect(self._on_cancel)

        button_layout.addWidget(self.btn_save)
        button_layout.addWidget(self.btn_cancel)

        layout.addLayout(button_layout)

    def _on_save(self):
        tokens = shlex.split(self.extra_options_edit.text()) if self.extra_options_edit.text().strip() else []
        self.options_saved.emit(tokens)

    def _on_cancel(self):
        self.options_cancelled.emit()
