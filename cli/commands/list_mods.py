from rich.console import Console

from backend.manager import Manager


def list_mods(manager: Manager, game_id: str) -> None:
    console = Console()
    mods = manager.get_mods(game_id)

    if not mods:
        console.print("No added mods found.")
        return

    console.print("[bold]Added mods[/bold]")

    for name, path in mods.items():
        console.print(f"  {name} - {path}")
