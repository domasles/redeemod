from typing import cast

from backend.games.base import BaseGameAdapter
from cli.commands.list_games import list_games


class FakeAdapter:
    display_name = "Fake Game"


def test_list_games_available(manager, capsys):
    adapters = cast(dict[str, BaseGameAdapter], {"fake": FakeAdapter()})

    list_games(manager, adapters, available=True)

    captured = capsys.readouterr()

    assert "fake" in captured.out
    assert "Fake Game" in captured.out


def test_list_games_added(manager, capsys):
    manager.add_game("fake")

    adapters = cast(dict[str, BaseGameAdapter], {"fake": FakeAdapter()})

    list_games(manager, adapters, available=False)

    captured = capsys.readouterr()

    assert "fake" in captured.out
    assert "Fake Game" in captured.out
