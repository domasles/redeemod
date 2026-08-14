from abc import ABC, abstractmethod
from dataclasses import fields
from pathlib import Path
from typing import List


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
    def required_path_keys(self) -> list[str]:
        """Required path keys parsed from config.json."""

        game_cfg = getattr(self, "config", None)
        cfg = game_cfg.games.get(self.game_id)

        return [
            f.name.removesuffix("_paths") + "_path"
            for f in fields(cfg)
            if f.name.endswith("_paths")
        ]

    def get_missing_paths(self) -> list[str]:
        """Checks all required_path_keys."""

        missing = []

        for key in self.required_path_keys:
            path_val = getattr(self, key, None)

            if not path_val or not Path(path_val).exists():
                missing.append(key)

        return missing

    @abstractmethod
    def launch(self, selected_mod_paths: List[Path]) -> None:
        """Prepares configuration/INI files and launches the executable."""
        pass

    @abstractmethod
    def scan_mod_directory(self, target_dir: Path) -> List[tuple[Path, str]]:
        """Scans a directory for valid mod files."""
        pass
