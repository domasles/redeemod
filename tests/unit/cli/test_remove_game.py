from backend.manager import Manager

from cli.commands.remove_game import remove_game


def test_remove_game(manager: Manager):
    manager.add_game("ut99")
    remove_game(manager, "ut99")

    assert manager.get_added_games() == []
