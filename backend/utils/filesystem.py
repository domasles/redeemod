from pathlib import Path


def is_path_valid(path: Path) -> bool:
    """Check if the given path is valid."""

    try:
        Path(path).resolve(strict=True)
        return True

    except Exception:
        return False


def get_base_directory(path: Path) -> Path:
    """Get the base directory of the given path."""

    if not is_path_valid(path):
        raise ValueError("Invalid path provided.")

    return Path(path).parent


def traverse_directory_by_extension(base_path: Path, extension: str) -> list[Path]:
    """Traverse the directory and return a list of files with the given extension."""

    if not is_path_valid(base_path):
        raise ValueError("Invalid base path provided.")

    return [file for file in Path(base_path).rglob(f'*.{extension}') if file.is_file()]


def get_relative_path(base_path: Path, target_path: Path) -> Path:
    """Get the relative path from base_path to target_path."""

    if not is_path_valid(base_path) or not is_path_valid(target_path):
        raise ValueError("Invalid path provided.")

    return Path(target_path).relative_to(base_path, walk_up=True)
