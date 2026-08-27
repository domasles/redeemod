from pathlib import Path

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QScrollArea,
    QFileDialog,
    QGridLayout,
    QSizePolicy,
    QSpacerItem,
)

from PySide6.QtCore import QObject, Qt

from backend.manager import Manager

from frontend.components.cards import GameCard, ModCard, ActionCard
from frontend.components.elided_label import ElidedLabel
from frontend.components.card import Card

from frontend.components.modals.message import show_error_modal, show_info_modal


class Library(QWidget):
    CARD_WIDTH = Card.CARD_WIDTH
    CARD_GAP = 20

    def __init__(self, parent: QObject, manager: Manager, adapters: dict):
        super().__init__(parent)

        self._last_width = 0
        self._cards: list[QWidget] = []

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

        self.title_label = ElidedLabel("Your mods")
        self.title_label.setObjectName("LibraryTitle")

        top_layout.addWidget(self.title_label)
        top_layout.addStretch()

        self.btn_back = QPushButton("Back to Games")
        self.btn_back.setObjectName("AddFolderBtn")
        self.btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_back.clicked.connect(self._go_back_to_games)

        sp_back = self.btn_back.sizePolicy()

        self.btn_back.setSizePolicy(sp_back)
        self.btn_back.setVisible(False)

        top_layout.addWidget(self.btn_back)

        self.btn_launch = QPushButton("Launch standalone")
        self.btn_launch.setObjectName("LaunchBtn")
        self.btn_launch.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_launch.clicked.connect(self._launch_game)

        sp_launch = self.btn_launch.sizePolicy()

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
            self._reposition_cards()

    def reset_state(self):
        self.selected_game_id = None
        self.selected_mods.clear()
        self.refresh_cards()

    def refresh_cards(self):
        self._clear_grid()
        self._cards.clear()

        if self.scroll_area.viewport().width() <= 0:
            return

        if self.selected_game_id is None:
            self._build_game_cards()

        else:
            self._build_mod_cards()

        self._reposition_cards()

    def _clear_grid(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

    def _build_game_cards(self):
        self.title_label.setText("Your mods")
        self.btn_back.setVisible(False)
        self.btn_launch.setVisible(False)

        added_games = self.manager.get_added_games()

        for game_id in added_games:
            adapter = self.adapters.get(game_id)

            name = adapter.display_name if adapter else game_id.upper()
            logo = adapter.logo if adapter and adapter.logo else None

            card = GameCard(self.scroll_content, name, "Select to manage mods", logo=logo)
            card.clicked.connect(lambda g_id=game_id: self._select_game(g_id))

            self._cards.append(card)

    def _build_mod_cards(self):
        adapter = self.adapters.get(self.selected_game_id)

        name = adapter.display_name if adapter else self.selected_game_id.upper()
        logo = adapter.logo if adapter and adapter.logo else None

        self.title_label.setText(f"Mods for {name}")
        self.btn_back.setVisible(True)
        self.btn_launch.setVisible(True)

        mods = self.manager.get_mods(self.selected_game_id)

        for mod_name, _ in mods.items():
            card = ModCard(
                self.scroll_content,
                mod_name,
                (mod_name in self.selected_mods),
                self._toggle_mod,
                self._delete_mod,
                logo=logo,
            )

            self._cards.append(card)

        add_card = ActionCard(self.scroll_content, "Add a mod", f"for {name}")
        add_card.clicked.connect(self._add_mod_dialog)
        self._cards.append(add_card)

        self._update_launch_button_text()

    def _reposition_cards(self):
        if not self._cards or self.scroll_area.viewport().width() <= 0:
            return

        self.setUpdatesEnabled(False)

        try:
            while self.grid_layout.count():
                self.grid_layout.takeAt(0)

            cols = self._get_columns_count()

            for c in range(cols):
                self.grid_layout.setColumnStretch(c, 0)

            for idx, card in enumerate(self._cards):
                row, col = idx // cols, idx % cols
                self.grid_layout.addWidget(card, row, col, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

            self.grid_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum), 0, cols)  # fmt: skip
            self.grid_layout.setColumnStretch(cols, 1)

            if self._cards:
                bottom_row = ((len(self._cards) - 1) // cols) + 1

                self.grid_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding), bottom_row, 0, 1, cols + 1)  # fmt: skip
                self.grid_layout.setRowStretch(bottom_row, 1)

        finally:
            self.setUpdatesEnabled(True)

    def _select_game(self, game_id: str):
        self.selected_game_id = game_id
        self.selected_mods.clear()
        self.refresh_cards()

    def _go_back_to_games(self):
        self.selected_game_id = None
        self.selected_mods.clear()
        self.refresh_cards()

    def _show_mod_limit_reached(self, adapter):
        amount = adapter.allowed_mod_amount
        unit = "mod" if amount == 1 else "mods"

        show_info_modal("Mod limit reached", f"{adapter.display_name} allows only {amount} {unit} to be selected.")

    def _toggle_mod(self, mod_name: str, enabled: bool):
        if enabled:
            adapter = self.adapters.get(self.selected_game_id) if self.selected_game_id else None

            if (
                adapter
                and adapter.allowed_mod_amount is not None
                and len(self.selected_mods) >= adapter.allowed_mod_amount
            ):
                self.refresh_cards()
                self._show_mod_limit_reached(adapter)

                return

            self.selected_mods.add(mod_name)

        else:
            self.selected_mods.discard(mod_name)

        all_mods = self.manager.get_mods(self.selected_game_id)

        if not Path(all_mods[mod_name]).exists():
            message = (
                f"The mod '{mod_name}' does not exist on disk.\n"
                "Remove it from your library or restore its folder."
            )  # fmt: skip

            self.selected_mods.discard(mod_name)
            self.refresh_cards()
            show_error_modal(message)

            return

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

            try:
                adapter.init_paths(custom_paths)

            except Exception as e:
                show_error_modal(str(e))
                return

            all_mods = self.manager.get_mods(self.selected_game_id)
            selected_paths = []

            for name in sorted(self.selected_mods):
                if name not in all_mods:
                    continue

                path = Path(all_mods[name])

                if path.exists():
                    selected_paths.append(path)

            try:
                adapter.launch(selected_paths)

            except Exception as e:
                show_error_modal(str(e))
