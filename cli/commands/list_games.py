from rich.console import Console

from backend.games.base import BaseGameAdapter
from backend.manager import Manager


def list_games(manager: Manager, adapters: dict[str, BaseGameAdapter], available: bool) -> None:
    console = Console()

    if available:
        console.print("[bold]Available games[/bold]")

        for game_id in sorted(adapters):
            adapter = adapters[game_id]
            console.print(f"  {game_id} - {adapter.display_name}")

        return

    added_games = manager.get_added_games()

    if not added_games:
        console.print("No added games found.")
        return

    console.print("[bold]Added games[/bold]")

    for game_id in added_games:
        adapter = adapters.get(game_id)
        display_name = adapter.display_name if adapter else game_id.upper()
        mod_count = len(manager.get_mods(game_id))
        console.print(f"  {game_id} - {display_name} ({mod_count} mods)")
