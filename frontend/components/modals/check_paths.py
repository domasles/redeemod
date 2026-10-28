from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Signal, Qt

from frontend.components.path_picker import PathPickerBody


class CheckPathsModalBody(QWidget):
    paths_confirmed = Signal(dict)

    def __init__(self, game_id: str, missing_path_keys: list[str]):
        super().__init__()

        self.setObjectName("CheckPathsModalBody")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.game_id = game_id
        self.missing_path_keys = list(missing_path_keys)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        info_label = QLabel(f"Some required paths were not found. Please locate them:")
        info_label.setObjectName("CardTitleLabel")
        info_label.setWordWrap(True)

        layout.addWidget(info_label)

        self.picker = PathPickerBody(self.missing_path_keys)
        self.picker.selection_changed.connect(self._on_selection_changed)
        layout.addWidget(self.picker)

        self.btn_add = QPushButton("Add selected game")
        self.btn_add.setObjectName("ConfirmBtn")
        self.btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_add.setEnabled(self.picker.validate())
        self.btn_add.clicked.connect(self._on_confirm)

        layout.addWidget(self.btn_add)

    def _on_selection_changed(self):
        self.btn_add.setEnabled(self.picker.validate())

    def _on_confirm(self):
        if self.picker.validate():
            self.paths_confirmed.emit(dict(self.picker.selected_paths))
