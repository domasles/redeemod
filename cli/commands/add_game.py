from rich.prompt import Prompt

from backend.games.base import BaseGameAdapter
from backend.manager import Manager


def add_game(
    manager: Manager,
    adapters: dict[str, BaseGameAdapter],
    game_id: str,
    set_paths: dict[str, str],
) -> None:
    adapter = adapters.get(game_id)

    if adapter is None:
        raise ValueError(f"Unknown game: {game_id}")

    custom_paths = dict(manager.get_custom_paths(game_id))
    missing = adapter.get_missing_paths()

    if missing:
        for key in missing:
            if set_paths.get(key):
                custom_paths[key] = set_paths[key]
                continue

            value = Prompt.ask(f"Path for '{key}'", default="")

            if value:
                custom_paths[key] = value

        manager.save_custom_paths(game_id, custom_paths)
        adapter.init_paths(custom_paths)
        missing = adapter.get_missing_paths()

    if missing:
        raise FileNotFoundError(f"Unable to add game '{game_id}', missing paths: {', '.join(missing)}")

    manager.add_game(game_id)

    if adapter.setup_message:
        adapter.setup()
