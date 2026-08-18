from .base import BaseGameAdapter

from .ut2k4.adapter import UT2K4GameAdapter
from .ut99.adapter import UT99GameAdapter


ADAPTERS: list[type[BaseGameAdapter]] = BaseGameAdapter.__subclasses__()


def get_adapter_class(game_id: str) -> type[BaseGameAdapter]:
    """Get adapter class by game ID."""

    for adapter_class in ADAPTERS:
        if adapter_class().game_id == game_id:
            return adapter_class

    raise ValueError(f"Unknown game ID: {game_id}")


def get_adapter_classes() -> dict[str, type[BaseGameAdapter]]:
    """Get all registered adapter classes."""
    return {adapter_class().game_id: adapter_class for adapter_class in ADAPTERS}
