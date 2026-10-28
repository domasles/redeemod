import shlex

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Signal, Qt

from backend.games.base import BaseGameAdapter

from frontend.components.path_picker import PathPickerBody


class SettingsModalBody(QWidget):
    options_saved = Signal(list)
    options_cancelled = Signal()
    paths_saved = Signal(dict)

    def __init__(
        self,
        game_id: str,
        options: list[str],
        adapter: BaseGameAdapter | None = None,
        custom_paths: dict[str, str] | None = None,
    ):
        super().__init__()

        self.setObjectName("SettingsModalBody")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.game_id = game_id
        self.options = list(options)
        self.adapter = adapter
        self.custom_paths = dict(custom_paths or {})
        self.picker: PathPickerBody | None = None

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

        initial_paths: dict[str, str] = {}

        if self.adapter is not None:
            for key in self.adapter.required_path_keys:
                resolved = self.adapter.resolved_path(key)
                value = self.custom_paths.get(key) or (str(resolved) if resolved is not None else "")

                if value:
                    initial_paths[key] = value

            paths_label = QLabel("Game paths:")
            paths_label.setObjectName("CardTitleLabel")
            paths_label.setWordWrap(True)

            layout.addWidget(paths_label)

            self.picker = PathPickerBody(self.adapter.required_path_keys, initial_paths=initial_paths)
            self.picker.selection_changed.connect(self._on_selection_changed)

            layout.addWidget(self.picker)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)

        self.btn_save = QPushButton("Done")
        self.btn_save.setObjectName("ConfirmBtn")
        self.btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_save.clicked.connect(self._on_save)

        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setObjectName("DenyBtn")
        self.btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cancel.clicked.connect(self._on_cancel)

        button_layout.addWidget(self.btn_save)
        button_layout.addWidget(self.btn_cancel)

        layout.addLayout(button_layout)
        self._update_save_state()

    def _on_selection_changed(self):
        self._update_save_state()

    def _update_save_state(self):
        if self.adapter is None or self.picker is None:
            self.btn_save.setEnabled(True)
            return

        self.btn_save.setEnabled(self.picker.validate())

    def _on_save(self):
        tokens = shlex.split(self.extra_options_edit.text()) if self.extra_options_edit.text().strip() else []
        self.options_saved.emit(tokens)

        if self.adapter is not None and self.picker is not None and self.picker.validate():
            self.paths_saved.emit(dict(self.picker.selected_paths))

    def _on_cancel(self):
        self.options_cancelled.emit()
