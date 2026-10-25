import shlex

from pathlib import Path

from backend.games.base import BaseGameAdapter
from backend.manager import Manager


def launch_game(
    manager: Manager,
    adapters: dict[str, BaseGameAdapter],
    game_id: str,
    mod_refs: list[str],
    extra_flags: str = "",
) -> None:
    adapter = adapters.get(game_id)

    if adapter is None or game_id not in manager.get_added_games():
        raise ValueError(f"Game is not added: {game_id}")

    mods = manager.get_mods(game_id)
    mod_paths: list[Path] = []

    for ref in mod_refs:
        mod_path = Path(mods[ref]) if ref in mods else Path(ref)

        if not mod_path.exists():
            raise FileNotFoundError(f"Mod path does not exist: {mod_path}")

        mod_paths.append(mod_path)

    if adapter.allowed_mod_amount is not None and len(mod_paths) > adapter.allowed_mod_amount:
        raise ValueError(f"{adapter.display_name} allows only {adapter.allowed_mod_amount} mod(s), got {len(mod_paths)}")  # fmt: skip

    extra_options = shlex.split(extra_flags) if extra_flags.strip() else []

    adapter.init_paths(manager.get_custom_paths(game_id))
    adapter.launch(mod_paths, extra_options)
