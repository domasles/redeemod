import sys
import os

from pathlib import Path


def get_project_directory() -> Path:
    """Returns base directory of the project."""

    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)

    return Path(__file__).resolve().parent.parent.parent


def get_base_directory(path: str | Path) -> Path:
    """Get the parent directory of a path."""
    return Path(path).parent


def expand_path(path: str | Path) -> Path:
    """Expands environment variables and user home."""

    expanded = os.path.expandvars(str(path))
    return Path(expanded).expanduser()


def traverse_directory_by_extension(base_path: str | Path, extension: str) -> list[Path]:
    """Traverse directory and return files matching extension."""

    path_obj = Path(base_path)

    if not path_obj.exists():
        raise ValueError(f"Base path does not exist: {base_path}")

    ext = extension.lstrip(".")
    return [f for f in path_obj.rglob(f"*.{ext}") if f.is_file()]


def get_relative_path(base_path: str | Path, target_path: str | Path) -> Path:
    """Get relative path from base_path to target_path."""
    return Path(target_path).relative_to(Path(base_path), walk_up=True)
