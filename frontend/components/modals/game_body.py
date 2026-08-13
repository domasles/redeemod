from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

from frontend.components.dropdown import Dropdown
from backend.games import get_adapter_classes


class AddGameModalBody(QWidget):
    def __init__(self, on_add: callable):
        super().__init__()

        layout = QVBoxLayout(self)

        self.combo = Dropdown()

        for game_id, adapter_class in get_adapter_classes().items():
            try:
                adapter = adapter_class()
                self.combo.addItem(adapter.display_name, game_id)

            except Exception:
                continue

        layout.addWidget(self.combo)

        btn = QPushButton("Add selected game")
        btn.setObjectName("LaunchBtn")
        btn.clicked.connect(lambda: on_add(self.combo.currentData()))

        layout.addWidget(btn)
