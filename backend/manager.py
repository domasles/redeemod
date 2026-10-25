import json

from collections.abc import Callable
from pathlib import Path

from backend.utils.filesystem import expand_path, get_app_data_directory
from backend.constants import *


class Manager:
    def __init__(self, storage_file: Path | None = None):
        if storage_file is None:
            storage_file = self._default_storage_file()

        self.storage_file = storage_file
        self.data: dict = {"games": [], "mods": {}, "paths": {}, "launch_options": {}}

        self._change_listeners: list[Callable[[], None]] = []

        self.load()

    @staticmethod
    def _default_storage_file() -> Path:
        storage_dir = get_app_data_directory(APP_NAME)
        storage_dir.mkdir(parents=True, exist_ok=True)

        return storage_dir / USER_SETTINGS_FILE_NAME

    def add_change_listener(self, listener: Callable[[], None]) -> None:
        self._change_listeners.append(listener)

    def remove_change_listener(self, listener: Callable[[], None]) -> None:
        if listener in self._change_listeners:
            self._change_listeners.remove(listener)

    def _notify_listeners(self) -> None:
        for listener in self._change_listeners.copy():
            listener()

    def add_game(self, game_id: str):
        if game_id not in self.data["games"]:
            self.data["games"].append(game_id)
            self.save()
            self._notify_listeners()

    def remove_game(self, game_id: str):
        if game_id in self.data["games"]:
            self.data["games"].remove(game_id)
            self.data["mods"].pop(game_id, None)
            self.data["paths"].pop(game_id, None)
            self.data["launch_options"].pop(game_id, None)

            self.save()
            self._notify_listeners()

    def add_mod(self, game_id: str, path_str: str) -> str:
        path = expand_path(path_str)
        mod_name = path.name

        if game_id not in self.data["mods"]:
            self.data["mods"][game_id] = {}

        self.data["mods"][game_id][mod_name] = str(path)
        self.save()

        return mod_name

    def remove_mod(self, game_id: str, mod_name: str):
        if game_id in self.data["mods"] and mod_name in self.data["mods"][game_id]:
            del self.data["mods"][game_id][mod_name]
            self.save()

    def save_custom_paths(self, game_id: str, paths: dict[str, str]):
        if "paths" not in self.data:
            self.data["paths"] = {}

        self.data["paths"][game_id] = paths
        self.save()

    def get_added_games(self) -> list[str]:
        return self.data.get("games", [])

    def get_mods(self, game_id: str) -> dict[str, str]:
        return self.data["mods"].get(game_id, {})

    def get_custom_paths(self, game_id: str) -> dict[str, str]:
        return self.data.get("paths", {}).get(game_id, {})

    def save_launch_options(self, game_id: str, options: list[str]):
        launch_options = self.data.setdefault("launch_options", {})
        launch_options[game_id] = list(options)

        self.save()

    def get_launch_options(self, game_id: str) -> list[str]:
        return list(self.data.get("launch_options", {}).get(game_id, []))

    def save(self):
        with open(self.storage_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)

    def load(self):
        if self.storage_file.exists():
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    self.data = json.load(f)

            except Exception:
                self.data = {"games": [], "mods": {}, "paths": {}, "launch_options": {}}
