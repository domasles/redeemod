import sys
import os

from pathlib import Path


def get_project_directory() -> Path:
    """Returns base directory of the project."""

    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)

    return Path(__file__).resolve().parent.parent.parent


def expand_path(path: str | Path) -> Path:
    """Expands environment variables and user home."""

    expanded = os.path.expandvars(str(path))
    return Path(expanded).expanduser()


def get_relative_path(base_path: str | Path, target_path: str | Path) -> Path:
    """Gets relative path from base_path to target_path."""
    return Path(target_path).relative_to(Path(base_path), walk_up=True)
