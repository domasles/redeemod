from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog
from PySide6.QtCore import Signal, Qt


class CheckPathsModalBody(QWidget):
    paths_confirmed = Signal(dict)

    def __init__(self, game_id: str, missing_path_keys: list[str], parent=None):
        super().__init__(parent)

        self.setObjectName("CheckPathsModalBody")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.game_id = game_id
        self.missing_path_keys = missing_path_keys
        self.selected_paths: dict[str, str] = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)

        info_label = QLabel(f"Some required paths were not found. Please locate them:")
        info_label.setObjectName("CardTitleLabel")
        info_label.setWordWrap(True)

        layout.addWidget(info_label)
        self.inputs: dict[str, QLineEdit] = {}

        for key in missing_path_keys:
            label_text = key.replace("_", " ").title()

            picker_layout = QHBoxLayout()
            picker_layout.setSpacing(8)

            line_edit = QLineEdit()
            line_edit.setObjectName("DropdownTrigger")
            line_edit.setReadOnly(True)
            line_edit.setPlaceholderText(f"Select {label_text}...")

            btn_browse = QPushButton("Browse")
            btn_browse.setObjectName("LaunchBtn")
            btn_browse.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_browse.clicked.connect(lambda _, k=key, le=line_edit: self._browse_file(k, le))

            picker_layout.addWidget(line_edit)
            picker_layout.addWidget(btn_browse)

            layout.addLayout(picker_layout)
            self.inputs[key] = line_edit

        self.btn_save = QPushButton("Add selected game")
        self.btn_save.setObjectName("LaunchBtn")
        self.btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_save.setEnabled(False)
        self.btn_save.clicked.connect(self._on_save)

        layout.addWidget(self.btn_save)

    def _browse_file(self, key: str, line_edit: QLineEdit):

        label_text = key.replace("_", " ").title()
        file_path, _ = QFileDialog.getOpenFileName(self, f"Select {label_text}")

        if file_path:
            line_edit.setText(file_path)
            self.selected_paths[key] = file_path
            self._validate_all()

    def _validate_all(self):
        all_filled = len(self.selected_paths) == len(self.missing_path_keys) and all(
            bool(path) for path in self.selected_paths.values()
        )

        self.btn_save.setEnabled(all_filled)

    def _on_save(self):
        self.paths_confirmed.emit(self.selected_paths)
