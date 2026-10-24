import pytest

from rich.prompt import Prompt
from typing import cast

from backend.games.base import BaseGameAdapter
from backend.manager import Manager

from cli.commands.add_game import add_game


class FakeAdapter:
    display_name = "Fake Game"
    setup_message = None
    custom_paths: dict = {}
    required_paths: list = []

    def __init__(self):
        self.setup_called = False

    def get_missing_paths(self):
        return [key for key in self.required_paths if not self.custom_paths.get(key)]

    def init_paths(self, custom_paths=None, config=None):
        self.custom_paths = dict(custom_paths or {})
        return None

    def setup(self):
        self.setup_called = True


def test_add_game_unknown_game_raises(manager: Manager):
    with pytest.raises(ValueError):
        add_game(manager, {}, "ut99", {})


def test_add_game_adds_game_when_setup_paths_resolved(manager: Manager):
    adapter = FakeAdapter()
    adapter.required_paths = ["executable_path"]
    adapter.custom_paths = {"executable_path": "/tmp/ut-bin"}

    add_game(manager, cast(dict[str, BaseGameAdapter], {"fake": adapter}), "fake", {"executable_path": "/tmp/ut-bin"})

    assert manager.get_added_games() == ["fake"]


def test_add_game_raises_when_missing_paths_remain(manager: Manager, monkeypatch):
    adapter = FakeAdapter()
    adapter.required_paths = ["executable_path", "config_path"]

    monkeypatch.setattr(Prompt, "ask", lambda *args, **kwargs: "")

    with pytest.raises(FileNotFoundError):
        add_game(manager, cast(dict[str, BaseGameAdapter], {"fake": adapter}), "fake", {"executable_path": "/tmp/ut-bin"})  # fmt: skip
