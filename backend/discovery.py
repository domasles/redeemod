import json
import sys

from typing import Dict, List
from pathlib import Path

from backend.utils.filesystem import expand_path
from backend.models import Config, GameConfig


def load_config(path: str | Path) -> Config:
    """Loads and parses the JSON configuration."""

    path = expand_path(path)

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return Config.from_dict(data)


def find_first_valid_path(paths: List[str]) -> Path | None:
    """Returns the first path that exists on disk."""

    for raw_path in paths:
        resolved_path = expand_path(raw_path)

        if resolved_path.exists():
            return resolved_path.resolve()

    return None


def _get_platform_key() -> str:
    """Determines the current platform key."""

    if sys.platform.startswith("linux"):
        return "linux"

    if sys.platform in ("win32", "cygwin"):
        return "windows"

    raise RuntimeError(f"Unsupported platform: {sys.platform}")


def discover_all_paths(game_config: GameConfig, custom_paths: Dict[str, str] | None = None) -> Dict[str, List[Path]]:
    """Discovers all configured paths for a game and merges custom paths."""

    discovered: Dict[str, List[Path]] = {}

    if not game_config or not hasattr(game_config, "paths"):
        return discovered

    platform_key = _get_platform_key()

    # Load pre-configured paths
    for path_key, platform_paths in game_config.paths.items():
        candidates = getattr(platform_paths, platform_key, [])
        discovered[path_key] = [expand_path(p) for p in candidates]

    # Merge custom path overrides
    for custom_key, custom_val in (custom_paths or {}).items():
        if not custom_val:
            continue

        target_key = (
            custom_key.removesuffix("_path") + "_paths"
            if custom_key.endswith("_path") and not custom_key.endswith("_paths")
            else custom_key
        )

        expanded = expand_path(custom_val)

        if target_key in discovered:
            if expanded not in discovered[target_key]:
                discovered[target_key].append(expanded)

        else:
            discovered[target_key] = [expanded]

    return discovered


def discover_installation(game_config: GameConfig, custom_paths: Dict[str, str] | None = None) -> Dict[str, Path | None]:  # fmt: skip
    """Discovers game installation based on configured data."""

    all_data = discover_all_paths(game_config, custom_paths)

    return {
        path_key.removesuffix("_paths") + "_path": find_first_valid_path([str(p) for p in paths])
        for path_key, paths in all_data.items()
    }
