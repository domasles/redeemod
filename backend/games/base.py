from abc import ABC, abstractmethod
from pathlib import Path

from backend.discovery import discover_all_paths, discover_installation, load_game_config
from backend.utils.filesystem import expand_path, get_project_directory


class BaseGameAdapter(ABC):
    """Abstract base class for all game adapters."""

    def __init__(self, custom_paths: dict[str, str] | None = None):
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
    def allowed_mod_amount(self) -> int | None:
        """Maximum number of mods selectable simultaneously, or None for unlimited."""
        return None

    @property
    def setup_message(self) -> str | None:
        """User-friendly description of what setup() does. Returning None skips the setup flow."""
        return None

    @property
    def required_path_keys(self) -> list[str]:
        """Required path keys parsed from config.json."""

        return [
            key.removesuffix("_paths") + "_path"
            for key in self.config.paths
            if key.endswith("_paths")
        ]  # fmt: skip

    @property
    def adapter_assets_path(self) -> Path | None:
        """Path to the game adapter assets directory."""
        return get_project_directory() / "backend" / "games" / self.game_id / "assets"

    def setup(self):
        """Optional initialization executed after adding the game, once the user confirms."""
        pass

    @abstractmethod
    def launch(self, selected_mod_paths: list[Path]):
        """Prepares configuration/INI files and launches the executable."""
        pass

    def init_paths(self, custom_paths: dict[str, str] | None = None):
        config_file = get_project_directory() / "backend" / "games" / self.game_id / "config" / "config.json"
        self.config = load_game_config(config_file)

        self.all_configured_data = discover_all_paths(self.config, custom_paths)

        for key, value in discover_installation(self.config, custom_paths).items():
            setattr(self, key, value)

    def get_missing_paths(self) -> list[str]:
        """Checks all required_path_keys."""

        missing = []

        for key in self.required_path_keys:
            path_val = getattr(self, key, None)

            if not path_val or not Path(path_val).exists():
                missing.append(key)

        return missing

    def scan_mod_directory(self, target_dir: Path) -> list[tuple[Path, str]]:
        """
        Returns pairs of (file_path, extension) of the scanned mod directory.
        Discards any file with an extension within self.file_extensions.
        """

        target_dir = expand_path(target_dir)
        mod_files = []

        if not target_dir.exists():
            return mod_files

        for item in target_dir.rglob("*"):
            if not item.is_file():
                continue

            ext = item.suffix.lstrip(".").lower()

            if self.file_extensions:
                if ext in self.file_extensions:
                    mod_files.append((item, ext))

            else:
                mod_files.append((item, ext))

        return mod_files
