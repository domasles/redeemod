import json
import sys
import os

from typing import Optional, Tuple
from pathlib import Path

from backend.models import Config


def expand_path(path: str | Path) -> Path:
    """Expands environment variables and user home."""

    expanded = os.path.expandvars(str(path))
    return Path(expanded).expanduser()


def load_config(path: str | Path) -> Config:
    """Loads and parses the JSON configuration."""

    path = expand_path(path)

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return Config.from_dict(data)


def find_first_valid_path(paths: list[str]) -> Optional[Path]:
    """Returns the first path that exists on disk."""

    for raw_path in paths:
        resolved_path = expand_path(raw_path)

        if resolved_path.exists():
            return resolved_path.resolve()

    return None


def discover_installation(config: Config) -> Tuple[Optional[Path], Optional[Path]]:
    """Detects the host OS and finds the matching executable and config file paths."""

    if sys.platform.startswith("linux"):
        exec_candidates = config.executable_paths.linux
        cfg_candidates = config.config_paths.linux

    elif sys.platform in ("win32", "cygwin"):
        exec_candidates = config.executable_paths.windows
        cfg_candidates = config.config_paths.windows

    else:
        raise RuntimeError(f"Unsupported platform: {sys.platform}")

    exe_path = find_first_valid_path(exec_candidates)
    cfg_path = find_first_valid_path(cfg_candidates)

    return exe_path, cfg_path
