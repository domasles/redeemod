from pathlib import Path

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QFileDialog, QGridLayout
from PySide6.QtCore import Qt

from frontend.components.card import Card


class Library(QWidget):
    CARD_WIDTH = 200
    CARD_GAP = 20

    def __init__(self, parent, mod_manager, game_adapter):
        super().__init__(parent)
        self.mod_manager = mod_manager
        self.game_adapter = game_adapter
        self.selected_mods: set[str] = set()
        self.last_cols = -1

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Top Control Bar
        top_bar = QWidget()
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(20, 20, 20, 10)

        title = QLabel("Mod Library")
        title.setObjectName("LibraryTitle")

        top_layout.addWidget(title)
        top_layout.addStretch()

        btn_add = QPushButton("+ Add Mod Folder")
        btn_add.setObjectName("AddFolderBtn")
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.clicked.connect(self._add_mod_dialog)

        top_layout.addWidget(btn_add)

        self.btn_launch = QPushButton("Launch standalone")
        self.btn_launch.setObjectName("LaunchBtn")
        self.btn_launch.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_launch.clicked.connect(self._launch_game)

        top_layout.addWidget(self.btn_launch)
        main_layout.addWidget(top_bar)

        # Scrollable Grid Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("LibraryScrollArea")
        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget()
        self.scroll_content.setObjectName("LibraryScrollContent")
        self.grid_layout = QGridLayout(self.scroll_content)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        self.grid_layout.setSpacing(self.CARD_GAP)

        self.scroll_area.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll_area)
        self.refresh_cards()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        container_width = self.scroll_area.viewport().width()

        if container_width <= 10:
            return

        cols = max(1, container_width // (self.CARD_WIDTH + self.CARD_GAP))

        if cols != self.last_cols:
            self.last_cols = cols
            self.refresh_cards()

    def refresh_cards(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        mods = self.mod_manager.get_mods()
        cols = max(1, self.last_cols)

        for c in range(cols + 1):
            self.grid_layout.setColumnStretch(c, 0)

        for idx, (mod_name, _) in enumerate(mods.items()):
            row = idx // cols
            col = idx % cols

            card = Card(
                self.scroll_content,
                mod_name=mod_name,
                is_selected=(mod_name in self.selected_mods),
                on_toggle=self._toggle_mod,
                on_delete=self._delete_mod,
            )

            self.grid_layout.addWidget(card, row, col, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.grid_layout.setColumnStretch(cols, 1)
        self._update_launch_button_text()

    def _toggle_mod(self, mod_name: str, enabled: bool):
        if enabled:
            self.selected_mods.add(mod_name)

        else:
            self.selected_mods.discard(mod_name)

        self._update_launch_button_text()

    def _delete_mod(self, mod_name: str):
        self.mod_manager.remove_mod(mod_name)
        self.selected_mods.discard(mod_name)
        self.refresh_cards()

    def _add_mod_dialog(self):
        path = QFileDialog.getExistingDirectory(self, "Select Mod Directory")

        if path:
            self.mod_manager.add_mod(path)
            self.refresh_cards()

    def _update_launch_button_text(self):
        if len(self.selected_mods) == 0:
            self.btn_launch.setText("Launch standalone")

        else:
            self.btn_launch.setText("Launch with mods")

    def _launch_game(self):
        all_mods = self.mod_manager.get_mods()
        selected_paths = [Path(all_mods[name]) for name in self.selected_mods if name in all_mods]
        self.game_adapter.launch(selected_paths)
