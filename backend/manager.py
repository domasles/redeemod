import json

from pathlib import Path
from typing import Dict

from backend.utils.filesystem import get_project_directory, expand_path


class Manager:
    def __init__(self, storage_file: Path = None):
        self.storage_file = storage_file or (get_project_directory() / "user_mods.json")
        self.mods: Dict[str, str] = {}
        self.load()

    def add_mod(self, path_str: str) -> str:
        path = expand_path(path_str)
        mod_name = path.name

        self.mods[mod_name] = str(path)
        self.save()

        return mod_name

    def remove_mod(self, mod_name: str) -> None:
        if mod_name in self.mods:
            del self.mods[mod_name]
            self.save()

    def get_mods(self) -> Dict[str, str]:
        return self.mods

    def save(self) -> None:
        with open(self.storage_file, "w", encoding="utf-8") as f:
            json.dump(self.mods, f, indent=4)

    def load(self) -> None:
        if self.storage_file.exists():
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    self.mods = json.load(f)

            except Exception:
                self.mods = {}
