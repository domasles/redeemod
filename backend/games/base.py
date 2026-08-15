from abc import ABC, abstractmethod
from dataclasses import fields
from pathlib import Path
from typing import List

from backend.utils.filesystem import expand_path


class BaseGameAdapter(ABC):
    """Abstract base class for all game adapters."""

    @property
    @abstractmethod
    def game_id(self) -> str:
        """Unique key for the game."""
        pass

    @property
    @abstractmethod
    def display_name(self) -> str:
        """User-friendly name."""
        pass

    @property
    def file_extensions(self) -> set[str]:
        """File extensions associated with the game."""
        pass

    @property
    def required_path_keys(self) -> list[str]:
        """Required path keys parsed from config.json."""

        game_cfg = getattr(self, "config", None)
        cfg = game_cfg.games.get(self.game_id)

        return [
            f.name.removesuffix("_paths") + "_path"
            for f in fields(cfg)
            if f.name.endswith("_paths")
        ]

    @abstractmethod
    def launch(self, selected_mod_paths: List[Path]) -> None:
        """Prepares configuration/INI files and launches the executable."""
        pass

    def get_missing_paths(self) -> list[str]:
        """Checks all required_path_keys."""

        missing = []

        for key in self.required_path_keys:
            path_val = getattr(self, key, None)

            if not path_val or not Path(path_val).exists():
                missing.append(key)

        return missing

    def scan_mod_directory(self, target_dir: Path) -> List[tuple[Path, str]]:
        target_dir = expand_path(target_dir)
        mod_files = []

        if not target_dir.exists():
            return mod_files

        for item in target_dir.rglob("*"):
            if not item.is_file():
                continue

            ext = item.suffix.lstrip(".").lower()

            if ext in self.file_extensions:
                mod_files.append((item, ext))

        return mod_files
