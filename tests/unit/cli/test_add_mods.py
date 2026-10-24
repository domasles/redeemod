from pathlib import Path
from typing import cast

import pytest

from backend.games.base import BaseGameAdapter
from backend.manager import Manager

from cli.commands.add_mods import add_mods


class FakeAdapter:
    display_name = "Fake Game"


def test_add_mods_unknown_game_raises(manager: Manager) -> None:
    with pytest.raises(ValueError):
        add_mods(manager, cast(dict[str, BaseGameAdapter], {}), "ut99", ["/tmp/mod-1"])


def test_add_mods_raises_when_game_not_added(manager: Manager, tmp_path: Path) -> None:
    adapter = FakeAdapter()

    with pytest.raises(ValueError):
        add_mods(manager, cast(dict[str, BaseGameAdapter], {"fake": adapter}), "fake", [str(tmp_path / "mod-1")])


def test_add_mods_adds_existing_mod_paths(manager: Manager, tmp_path: Path) -> None:
    manager.add_game("fake")

    adapter = FakeAdapter()
    mod_1 = tmp_path / "mod-1"
    mod_1.mkdir()

    add_mods(manager, cast(dict[str, BaseGameAdapter], {"fake": adapter}), "fake", [str(mod_1)])
    assert "mod-1" in manager.get_mods("fake")
