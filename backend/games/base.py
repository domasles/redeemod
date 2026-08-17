from abc import ABC, abstractmethod
from typing import Dict, List, Any
from pathlib import Path

from backend.utils.filesystem import expand_path, get_project_directory
from backend.discovery import discover_all_paths, load_config


class BaseGameAdapter(ABC):
    """Abstract base class for all game adapters."""

    def __init__(self, custom_paths: Dict[str, Any] | None = None):
        self.init_paths(custom_paths)

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
    def logo(self) -> Path | None:
        """Path to the game's logo image."""
        pass

    @property
    def file_extensions(self) -> set[str]:
        """File extensions associated with the game."""
        pass

    @property
    def required_path_keys(self) -> list[str]:
        """Required path keys parsed from config.json."""

        game_cfg = getattr(self, "config", None)
        cfg = game_cfg.games.get(self.game_id) if game_cfg else None

        if not cfg or not hasattr(cfg, "paths"):
            return []

        return [
            key.removesuffix("_paths") + "_path"
            for key in cfg.paths.keys()
            if key.endswith("_paths")
        ]

    @property
    def adapter_assets_path(self) -> Path | None:
        """Path to the game adapter assets directory."""
        return get_project_directory() / "backend/games" / self.game_id / "assets"

    @abstractmethod
    def launch(self, selected_mod_paths: List[Path]) -> None:
        """Prepares configuration/INI files and launches the executable."""
        pass

    def init_paths(self, custom_paths: Dict[str, Any] | None = None) -> None:
        config_file = get_project_directory() / "backend/config/config.json"
        self.config = load_config(config_file)

        custom_paths = custom_paths or {}
        game_cfg = self.config.games.get(self.game_id)

        self.all_configured_data = (discover_all_paths(game_cfg, custom_paths) if game_cfg else {})

        for key, value in self.all_configured_data.items():
            if key.endswith("_paths"):
                singular_key = key.removesuffix("_paths") + "_path"
                custom_val = custom_paths.get(singular_key)

                if custom_val:
                    setattr(self, singular_key, expand_path(custom_val))

                else:
                    valid_path = None
                    paths_list = value if isinstance(value, list) else [value]

                    for p in paths_list:
                        if isinstance(p, (str, Path)) and Path(p).exists():
                            valid_path = Path(p)
                            break

                    if not valid_path and paths_list:
                        valid_path = Path(paths_list[0]) if isinstance(paths_list[0], (str, Path)) else paths_list[0]

                    setattr(self, singular_key, valid_path)

            else:
                setattr(self, key, value)

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
