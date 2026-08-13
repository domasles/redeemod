import json

from pathlib import Path

from PySide6.QtCore import QObject, Signal, QStandardPaths

from backend.utils.filesystem import expand_path
from backend.constants import *


class Manager(QObject):
    games_changed = Signal()

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)

        storage_dir = Path(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)) / APP_NAME
        storage_dir.mkdir(parents=True, exist_ok=True)

        self.storage_file = storage_dir / USER_SETTINGS_FILE_NAME
        self.data: dict = {"games": [], "mods": {}}

        self.load()

    def get_added_games(self) -> list[str]:
        return self.data.get("games", [])

    def add_game(self, game_id: str) -> None:
        if game_id not in self.data["games"]:
            self.data["games"].append(game_id)
            self.save()
            self.games_changed.emit()

    def remove_game(self, game_id: str) -> None:
        if game_id in self.data["games"]:
            self.data["games"].remove(game_id)
            self.data["mods"].pop(game_id, None)

            self.save()

            self.games_changed.emit()

    def add_mod(self, game_id: str, path_str: str) -> str:
        path = expand_path(path_str)
        mod_name = path.name

        if game_id not in self.data["mods"]:
            self.data["mods"][game_id] = {}

        self.data["mods"][game_id][mod_name] = str(path)
        self.save()

        return mod_name

    def remove_mod(self, game_id: str, mod_name: str) -> None:
        if game_id in self.data["mods"] and mod_name in self.data["mods"][game_id]:
            del self.data["mods"][game_id][mod_name]
            self.save()

    def get_mods(self, game_id: str) -> dict[str, str]:
        return self.data["mods"].get(game_id, {})

    def save(self) -> None:
        with open(self.storage_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)

    def load(self) -> None:
        if self.storage_file.exists():
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    self.data = json.load(f)

            except Exception:
                self.data = {"games": [], "mods": {}}
