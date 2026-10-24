from backend.manager import Manager


def remove_game(manager: Manager, game_id: str) -> None:
    manager.remove_game(game_id)
