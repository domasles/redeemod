from pathlib import Path

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea, QFileDialog, QGridLayout, QSizePolicy, QSpacerItem
from PySide6.QtCore import QObject, Qt

from backend.manager import Manager

from frontend.components.cards import GameCard, ModCard, ActionCard
from frontend.components.elided_label import ElidedLabel
from frontend.components.card import Card


class Library(QWidget):
    CARD_WIDTH = Card.CARD_WIDTH
    CARD_GAP = 20

    def __init__(self, parent: QObject, manager: Manager, adapters: dict):
        super().__init__(parent)

        self._last_width = 0

        self.manager = manager
        self.adapters = adapters
        self.selected_game_id: str | None = None
        self.selected_mods: set[str] = set()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        top_bar = QWidget()
        top_bar.setFixedHeight(65)

        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(20, 15, 20, 10)

        self.title_label = ElidedLabel("Mod Library")
        self.title_label.setObjectName("LibraryTitle")

        top_layout.addWidget(self.title_label)
        top_layout.addStretch()

        self.btn_back = QPushButton("Back to Games")
        self.btn_back.setObjectName("AddFolderBtn")
        self.btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_back.clicked.connect(self._go_back_to_games)

        sp_back = self.btn_back.sizePolicy()
        sp_back.setRetainSizeWhenHidden(True)

        self.btn_back.setSizePolicy(sp_back)
        self.btn_back.setVisible(False)

        top_layout.addWidget(self.btn_back)

        self.btn_launch = QPushButton("Launch standalone")
        self.btn_launch.setObjectName("LaunchBtn")
        self.btn_launch.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_launch.clicked.connect(self._launch_game)

        sp_launch = self.btn_launch.sizePolicy()
        sp_launch.setRetainSizeWhenHidden(True)

        self.btn_launch.setSizePolicy(sp_launch)
        self.btn_launch.setVisible(False)

        top_layout.addWidget(self.btn_launch)
        main_layout.addWidget(top_bar)

        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("LibraryScrollArea")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.scroll_content = QWidget()
        self.scroll_content.setObjectName("LibraryScrollContent")

        self.grid_layout = QGridLayout(self.scroll_content)
        self.grid_layout.setContentsMargins(20, 10, 20, 10)
        self.grid_layout.setHorizontalSpacing(self.CARD_GAP)
        self.grid_layout.setVerticalSpacing(self.CARD_GAP)

        self.scroll_area.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll_area)

    def _get_columns_count(self) -> int:
        viewport_width = self.scroll_area.viewport().width() - 40

        if viewport_width <= 0:
            return 3

        return max(1, viewport_width // (self.CARD_WIDTH + self.CARD_GAP))

    def showEvent(self, event):
        super().showEvent(event)
        self.refresh_cards()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        current_width = self.scroll_area.viewport().width()

        if current_width > 0 and abs(current_width - self._last_width) > 10:
            self._last_width = current_width
            self.refresh_cards()

    def reset_state(self):
        self.selected_game_id = None
        self.selected_mods.clear()
        self.refresh_cards()

    def refresh_cards(self):
        if self.scroll_area.viewport().width() <= 0:
            return

        self.setUpdatesEnabled(False)

        try:
            while self.grid_layout.count():
                item = self.grid_layout.takeAt(0)

                if item.widget():
                    item.widget().deleteLater()

            cols = self._get_columns_count()

            for c in range(cols):
                self.grid_layout.setColumnStretch(c, 0)

            if self.selected_game_id is None:
                idx = self._render_game_selection(cols)

            else:
                idx = self._render_mod_selection(cols)

            self.grid_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum), 0, cols)
            self.grid_layout.setColumnStretch(cols, 1)

            if idx > 0:
                bottom_row = ((idx - 1) // cols) + 1

                self.grid_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding), bottom_row, 0, 1, cols + 1)
                self.grid_layout.setRowStretch(bottom_row, 1)

        finally:
            self.setUpdatesEnabled(True)

    def _render_game_selection(self, cols: int) -> int:
        self.title_label.setText("Your mods")
        self.btn_back.setVisible(False)
        self.btn_launch.setVisible(False)

        added_games = self.manager.get_added_games()
        idx = 0

        for game_id in added_games:
            adapter = self.adapters.get(game_id)

            name = adapter.display_name if adapter else game_id.upper()
            logo = adapter.logo if adapter and adapter.logo else None

            card = GameCard(self.scroll_content, name, "Select to manage mods", logo=logo)
            card.clicked.connect(lambda g_id=game_id: self._select_game(g_id))

            row, col = idx // cols, idx % cols
            self.grid_layout.addWidget(card, row, col, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
            idx += 1

        return idx

    def _render_mod_selection(self, cols: int) -> int:
        adapter = self.adapters.get(self.selected_game_id)

        name = adapter.display_name if adapter else self.selected_game_id.upper()
        logo = adapter.logo if adapter and adapter.logo else None

        self.title_label.setText(f"Mods for {name}")
        self.btn_back.setVisible(True)
        self.btn_launch.setVisible(True)

        mods = self.manager.get_mods(self.selected_game_id)
        idx = 0

        for mod_name, _ in mods.items():
            card = ModCard(
                self.scroll_content,
                mod_name,
                (mod_name in self.selected_mods),
                self._toggle_mod,
                self._delete_mod,
                logo=logo,
            )

            row, col = idx // cols, idx % cols
            self.grid_layout.addWidget(card, row, col, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
            idx += 1

        add_card = ActionCard(self.scroll_content, "Add a mod", f"for {name}")
        add_card.clicked.connect(self._add_mod_dialog)

        row, col = idx // cols, idx % cols
        self.grid_layout.addWidget(add_card, row, col, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        idx += 1

        self._update_launch_button_text()

        return idx

    def _select_game(self, game_id: str):
        self.selected_game_id = game_id
        self.selected_mods.clear()
        self.refresh_cards()

    def _go_back_to_games(self):
        self.selected_game_id = None
        self.selected_mods.clear()
        self.refresh_cards()

    def _toggle_mod(self, mod_name: str, enabled: bool):
        if enabled:
            self.selected_mods.add(mod_name)

        else:
            self.selected_mods.discard(mod_name)

        self._update_launch_button_text()

    def _delete_mod(self, mod_name: str):
        if self.selected_game_id:
            self.manager.remove_mod(self.selected_game_id, mod_name)
            self.selected_mods.discard(mod_name)
            self.refresh_cards()

    def _pick_directory(self) -> str:
        return QFileDialog.getExistingDirectory(caption="Select Mod Directory")

    def _add_mod_dialog(self):
        if self.selected_game_id:
            path = self._pick_directory()

            if path:
                adapter = self.adapters.get(self.selected_game_id)

                if adapter and adapter.scan_mod_directory(Path(path)):
                    self.manager.add_mod(self.selected_game_id, path)
                    self.refresh_cards()

    def _update_launch_button_text(self):
        if len(self.selected_mods) == 0:
            self.btn_launch.setText("Launch standalone")

        else:
            self.btn_launch.setText("Launch with mods")

    def _launch_game(self):
        if not self.selected_game_id:
            return

        adapter = self.adapters.get(self.selected_game_id)

        if adapter:
            custom_paths = self.manager.get_custom_paths(self.selected_game_id)
            adapter.init_paths(custom_paths)

            all_mods = self.manager.get_mods(self.selected_game_id)
            selected_paths = [Path(all_mods[name]) for name in self.selected_mods if name in all_mods]
            adapter.launch(selected_paths)
