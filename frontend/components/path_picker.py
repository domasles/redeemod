from pathlib import Path

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QFileDialog
from PySide6.QtCore import Signal, Qt


class PathPickerBody(QWidget):
    """Browse and select one or more game paths."""

    selection_changed = Signal()

    def __init__(self, path_keys: list[str], initial_paths: dict[str, str] | None = None):
        super().__init__()

        self.setObjectName("PathPickerBody")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.path_keys = list(path_keys)
        self.selected_paths: dict[str, str] = {key: value for key, value in (initial_paths or {}).items() if value}

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        self.inputs: dict[str, QLineEdit] = {}
        self.btn_browses: dict[str, QPushButton] = {}

        for key in self.path_keys:
            label_text = key.replace("_", " ").title()

            picker_layout = QHBoxLayout()
            picker_layout.setSpacing(8)

            line_edit = QLineEdit()
            line_edit.setObjectName("DropdownTrigger")
            line_edit.setReadOnly(True)
            line_edit.setText(self.selected_paths.get(key, ""))
            line_edit.setPlaceholderText(f"Select {label_text}...")

            btn_browse = QPushButton("Browse")
            btn_browse.setObjectName("ConfirmBtn")
            btn_browse.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_browse.clicked.connect(lambda _, k=key, le=line_edit: self._browse(k, le))

            picker_layout.addWidget(line_edit)
            picker_layout.addWidget(btn_browse)

            layout.addLayout(picker_layout)
            self.inputs[key] = line_edit
            self.btn_browses[key] = btn_browse

    def _browse(self, key: str, line_edit: QLineEdit) -> None:
        label_text = key.replace("_", " ").title()
        file_path, _ = QFileDialog.getOpenFileName(caption=f"Select {label_text}")

        if file_path:
            resolved_path = Path(file_path).resolve()

            if resolved_path.exists():
                resolved_str = str(resolved_path)
                line_edit.setText(resolved_str)
                self.selected_paths[key] = resolved_str

            else:
                line_edit.clear()
                self.selected_paths.pop(key, None)

        self.selection_changed.emit()

    def validate(self) -> bool:
        return len(self.selected_paths) >= len(self.path_keys) and all(
            self.selected_paths.get(key) for key in self.path_keys
        )
