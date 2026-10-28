import argparse

from rich.console import Console

from backend.games.base import BaseGameAdapter
from backend.games import get_adapter_classes
from backend.manager import Manager

from cli.commands import add_game, add_mods, launch_game, list_games, list_mods, remove_game, remove_mods


def build_parser() -> argparse.ArgumentParser:
    # fmt: off
    parser = argparse.ArgumentParser(
        prog="redeemod-cli",
        description="RedeeMOD - a custom game launcher with modding capabilities.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list-games", help="List added games, or all available with --available.")
    list_parser.add_argument(
        "--available",
        action="store_true",
        help="List all available games."
    )

    add_parser = subparsers.add_parser("add-game", help="Add a game to the library.")
    add_parser.add_argument("game_id", help="Game's ID to add.")
    add_parser.add_argument(
        "--set-path",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Manually set up a path, overriding discovered defaults.",
    )

    remove_parser = subparsers.add_parser("remove-game", help="Remove a game from the library.")
    remove_parser.add_argument("game_id", help="Game's ID to reset preferences of.")

    list_mods_parser = subparsers.add_parser("list-mods", help="List added mods for a game.")
    list_mods_parser.add_argument("game_id", help="Already added game's ID.")

    add_mods_parser = subparsers.add_parser("add-mods", help="Add mod directory paths to a game.")
    add_mods_parser.add_argument("game_id", help="Already added game's ID.")
    add_mods_parser.add_argument(
        "mod_paths",
        nargs="*",
        default=[],
        help="Existing mod directory paths to add."
    )

    remove_mods_parser = subparsers.add_parser("remove-mods", help="Remove mods from a game by name or path.")
    remove_mods_parser.add_argument("game_id", help="Already added game's ID.")
    remove_mods_parser.add_argument(
        "mod_refs",
        nargs="*",
        default=[],
        help="Mod names or paths to remove."
    )

    launch_parser = subparsers.add_parser("launch", help="Launch a game, optionally with mod names or paths.")
    launch_parser.add_argument("game_id", help="Already added game's ID.")
    launch_parser.add_argument(
        "mod_refs",
        nargs="*",
        default=[],
        help="Mod names or existing mod directory paths to launch with."
    )
    launch_parser.add_argument(
        "--flags",
        type=str,
        default="",
        help="Extra launch options."
    )
    # fmt: on

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    manager = Manager()
    adapters: dict[str, BaseGameAdapter] = {}

    for game_id, adapter_class in get_adapter_classes().items():
        try:
            adapters[game_id] = adapter_class()

        except Exception:
            continue

    console = Console()

    try:
        if args.command == "list-games":
            list_games(manager, adapters, available=args.available)

        elif args.command == "add-game":
            set_paths: dict[str, str] = {}

            for raw in args.set_path or []:
                key, separator, value = raw.partition("=")

                if separator and key and value:
                    set_paths[key] = value

            add_game(manager, adapters, args.game_id, set_paths)

        elif args.command == "remove-game":
            remove_game(manager, args.game_id)

        elif args.command == "list-mods":
            list_mods(manager, args.game_id)

        elif args.command == "add-mods":
            add_mods(manager, adapters, args.game_id, args.mod_paths)

        elif args.command == "remove-mods":
            remove_mods(manager, args.game_id, args.mod_refs)

        elif args.command == "launch":
            launch_game(manager, adapters, args.game_id, args.mod_refs, args.flags)

    except Exception as error:
        console.print(f"[red]Error:[/red] {error}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
