import json
import sys

from pathlib import Path

from backend.utils.filesystem import expand_path
from backend.models import GameConfig


def load_game_config(path: str | Path) -> GameConfig:
    """Loads and parses a per-game JSON configuration."""

    path = expand_path(path)

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return GameConfig.from_dict(data)


def _get_platform_key() -> str:
    """Determines the current platform key."""

    if sys.platform.startswith("linux"):
        return "linux"

    if sys.platform in ("win32", "cygwin"):
        return "windows"

    raise RuntimeError(f"Unsupported platform: {sys.platform}")


def discover_all_paths(
    game_config: GameConfig,
    custom_paths: dict[str, str] | None = None,
    platform_key: str | None = None,
) -> dict[str, list[Path]]:
    """Discovers all configured path candidates for a game and merges custom overrides."""

    discovered: dict[str, list[Path]] = {}

    if not game_config:
        return discovered

    platform_key = platform_key or _get_platform_key()

    for path_key, platform_paths in game_config.paths.items():
        candidates = getattr(platform_paths, platform_key, [])
        discovered[path_key] = [expand_path(p) for p in candidates]

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
                discovered[target_key].insert(0, expanded)

        else:
            discovered[target_key] = [expanded]

    return discovered


def discover_installation(
    game_config: GameConfig,
    custom_paths: dict[str, str] | None = None,
    platform_key: str | None = None,
) -> dict[str, Path | None]:
    """Resolves every configured path group to a single usable path."""

    resolved: dict[str, Path | None] = {}

    for path_key, candidates in discover_all_paths(game_config, custom_paths, platform_key).items():
        singular_key = path_key.removesuffix("_paths") + "_path"
        custom_val = (custom_paths or {}).get(singular_key)

        if custom_val:
            resolved[singular_key] = expand_path(custom_val)
            continue

        valid_path = next((p for p in candidates if p.exists()), None)
        resolved[singular_key] = valid_path.resolve() if valid_path else candidates[0].resolve() if candidates else None

    return resolved
