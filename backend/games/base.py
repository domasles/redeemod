import subprocess

from abc import ABC, abstractmethod
from pathlib import Path
from typing import final

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
        return set()

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
            for key in self._config.paths
            if key.endswith("_paths")
        ]  # fmt: skip

    @property
    def adapter_assets_path(self) -> Path:
        """Path to the game adapter assets directory."""
        return get_project_directory() / "backend" / "games" / self.game_id / "assets"

    def setup(self):
        """Optional initialization executed after adding the game, once the user confirms."""
        pass

    @abstractmethod
    def build_arguments(self, executable: Path, selected_mod_paths: list[Path]) -> list[str]:
        """Builds the extra command-line arguments for the game executable."""
        pass

    @final
    def launch(self, selected_mod_paths: list[Path]):
        """Launches the executable with extra arguments (if provided)"""

        executable = self.resolved_path("executable_path")

        if not executable or not executable.exists():
            raise FileNotFoundError(f"{self.display_name} installation not found.")

        cmd = [str(executable), *self.build_arguments(executable, selected_mod_paths)]

        subprocess.Popen(cmd, cwd=str(executable.parent))

    def init_paths(self, custom_paths: dict[str, str] | None = None):
        """(Re)loads configuration and resolves paths."""

        config_file = get_project_directory() / "backend" / "games" / self.game_id / "config" / "config.json"

        self._config = load_game_config(config_file)
        self._all_configured_data = discover_all_paths(self._config, custom_paths)
        self._resolved_paths = discover_installation(self._config, custom_paths)

    def resolved_path(self, key: str) -> Path | None:
        """Returns a single resolved path for ``config.json`` key, or ``None``."""
        return self._resolved_paths.get(key)

    def resolved_paths(self, key: str) -> list[Path]:
        """Returns every configured candidate path from ``config.key`` or ``[]``."""
        return self._all_configured_data.get(key, [])

    def get_missing_paths(self) -> list[str]:
        """Checks all required_path_keys."""

        missing = []

        for key in self.required_path_keys:
            path_val = self.resolved_path(key)

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
