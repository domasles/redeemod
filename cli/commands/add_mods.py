from pathlib import Path

from backend.games.base import BaseGameAdapter
from backend.manager import Manager


def add_mods(manager: Manager, adapters: dict[str, BaseGameAdapter], game_id: str, mod_paths: list[str]) -> None:
    adapter = adapters.get(game_id)

    if adapter is None or game_id not in manager.get_added_games():
        raise ValueError(f"Game is not added: {game_id}")

    for mod_path_str in mod_paths:
        mod_path = Path(mod_path_str)

        if not mod_path.exists():
            raise FileNotFoundError(f"Mod path does not exist: {mod_path}")

        manager.add_mod(game_id, str(mod_path))
