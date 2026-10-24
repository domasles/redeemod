from pathlib import Path
from typing import cast

import pytest

from backend.games.base import BaseGameAdapter
from backend.manager import Manager

from cli.commands.launch_game import launch_game


class FakeAdapter:
    display_name = "Fake Game"
    allowed_mod_amount: int | None = 1
    custom_paths: dict = {}

    def __init__(self):
        self.launched: list[list[Path]] = []

    def get_missing_paths(self):
        return []

    def init_paths(self, custom_paths=None, config=None):
        self.custom_paths = dict(custom_paths or {})
        return None

    def launch(self, selected_mod_paths):
        self.launched.append(list(selected_mod_paths))
        return None


def test_launch_game_not_added(manager: Manager):
    adapter = FakeAdapter()

    with pytest.raises(ValueError):
        launch_game(manager, cast(dict[str, BaseGameAdapter], {"fake": adapter}), "fake", [])


def test_launch_game_missing_mod_path_raises(manager: Manager, tmp_path: Path):
    manager.add_game("fake")
    adapter = FakeAdapter()

    with pytest.raises(FileNotFoundError):
        launch_game(manager, cast(dict[str, BaseGameAdapter], {"fake": adapter}), "fake", [str(tmp_path / "missing-mod")])  # fmt: skip


def test_launch_game_respects_allowed_mod_amount(manager: Manager, tmp_path: Path):
    manager.add_game("fake")

    adapter = FakeAdapter()
    adapter.allowed_mod_amount = 1

    mod_1 = tmp_path / "mod-1"
    mod_2 = tmp_path / "mod-2"

    mod_1.mkdir()
    mod_2.mkdir()

    with pytest.raises(ValueError):
        launch_game(manager, cast(dict[str, BaseGameAdapter], {"fake": adapter}), "fake", [str(mod_1), str(mod_2)])


def test_launch_game_launches_with_mods(manager: Manager, tmp_path: Path):
    manager.add_game("fake")

    adapter = FakeAdapter()
    adapter.allowed_mod_amount = None

    mod_1 = tmp_path / "mod-1"
    mod_2 = tmp_path / "mod-2"

    mod_1.mkdir()
    mod_2.mkdir()

    launch_game(manager, cast(dict[str, BaseGameAdapter], {"fake": adapter}), "fake", [str(mod_1), str(mod_2)])
    assert adapter.launched == [[mod_1, mod_2]]


def test_launch_game_resolves_mod_name_to_path(manager: Manager, tmp_path: Path) -> None:
    manager.add_game("fake")

    adapter = FakeAdapter()
    adapter.allowed_mod_amount = None

    mod_1 = tmp_path / "mod-1"
    mod_1.mkdir()

    manager.add_mod("fake", str(mod_1))
    launch_game(manager, cast(dict[str, BaseGameAdapter], {"fake": adapter}), "fake", ["mod-1"])

    assert adapter.launched == [[mod_1]]


def test_launch_game_standalone_launches_without_mods(manager: Manager) -> None:
    manager.add_game("fake")

    adapter = FakeAdapter()
    adapter.allowed_mod_amount = None

    launch_game(manager, cast(dict[str, BaseGameAdapter], {"fake": adapter}), "fake", [])
    assert adapter.launched == [[]]
