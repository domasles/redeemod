import importlib

from pathlib import Path

from .base import BaseGameAdapter


def _load_adapters() -> None:
    """Imports every game adapter and registers its subclasses."""

    package_dir = Path(__file__).resolve().parent

    for child in sorted(package_dir.iterdir()):
        if not child.is_dir() or child.name.startswith("_"):
            continue

        if not (child / "adapter.py").is_file():
            continue

        module_name = f"{__name__}.{child.name}.adapter"

        try:
            importlib.import_module(module_name)

        except ModuleNotFoundError as e:
            if e.name == module_name:
                continue

            raise


_load_adapters()
ADAPTERS: list[type[BaseGameAdapter]] = BaseGameAdapter.__subclasses__()


def get_adapter_class(game_id: str) -> type[BaseGameAdapter]:
    """Gets adapter class by game ID."""

    for adapter_class in ADAPTERS:
        if adapter_class().game_id == game_id:
            return adapter_class

    raise ValueError(f"Unknown game ID: {game_id}")


def get_adapter_classes() -> dict[str, type[BaseGameAdapter]]:
    """Gets all registered adapter classes."""
    return {adapter_class().game_id: adapter_class for adapter_class in ADAPTERS}
