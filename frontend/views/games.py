from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QGridLayout, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt

from frontend.components.modals.game_body import AddGameModalBody
from frontend.components.cards import GameCard, ActionCard
from frontend.components.modal import ModalDialog
from frontend.components.card import Card


class Games(QWidget):
    CARD_WIDTH = Card.CARD_WIDTH
    CARD_GAP = 20

    def __init__(self, parent, manager, adapters: dict):
        super().__init__(parent)

        self.manager = manager
        self.adapters = adapters

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        top_bar = QWidget()
        top_bar.setFixedHeight(65)

        top_layout = QVBoxLayout(top_bar)
        top_layout.setContentsMargins(20, 15, 20, 10)

        title = QLabel("Installed games")
        title.setObjectName("LibraryTitle")

        top_layout.addWidget(title)
        layout.addWidget(top_bar)

        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("LibraryScrollArea")
        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget()
        self.scroll_content.setObjectName("LibraryScrollContent")

        self.grid_layout = QGridLayout(self.scroll_content)
        self.grid_layout.setContentsMargins(20, 10, 20, 10)
        self.grid_layout.setHorizontalSpacing(self.CARD_GAP)
        self.grid_layout.setVerticalSpacing(self.CARD_GAP)

        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)
        self.refresh_games()

    def _get_columns_count(self) -> int:
        viewport_width = self.scroll_area.viewport().width() - 40

        if viewport_width <= 0:
            return 3

        return max(1, viewport_width // (self.CARD_WIDTH + self.CARD_GAP))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.refresh_games()

    def refresh_games(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        cols = self._get_columns_count()

        for c in range(cols):
            self.grid_layout.setColumnStretch(c, 0)

        added_games = self.manager.get_added_games()
        idx = 0

        for game_id in added_games:
            adapter = self.adapters.get(game_id)
            name = adapter.display_name if adapter else game_id.upper()

            card = GameCard(
                self.scroll_content,
                display_name=name,
                subtitle="Add mods in Library",
                on_delete=lambda g_id=game_id: self._remove_game(g_id)
            )

            row, col = idx // cols, idx % cols
            self.grid_layout.addWidget(card, row, col, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
            idx += 1

        add_card = ActionCard(self.scroll_content, title="Add game", subtitle="to your start modding")
        add_card.clicked.connect(self._open_add_game_modal)
        row, col = idx // cols, idx % cols

        self.grid_layout.addWidget(add_card, row, col, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        idx += 1

        self.grid_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum), 0, cols)
        self.grid_layout.setColumnStretch(cols, 1)

        if idx > 0:
            bottom_row = ((idx - 1) // cols) + 1

            self.grid_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding), bottom_row, 0, 1, cols + 1)
            self.grid_layout.setRowStretch(bottom_row, 1)

    def _remove_game(self, game_id: str):
        self.manager.remove_game(game_id)
        self.refresh_games()

    def _open_add_game_modal(self):
        def handle_add(game_id: str):
            self.manager.add_game(game_id)
            modal.accept()
            self.refresh_games()

        body = AddGameModalBody(on_add=handle_add)
        modal = ModalDialog(self, title="Select game", body_widget=body)
        modal.exec()
