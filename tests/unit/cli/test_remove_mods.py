import pytest

from backend.manager import Manager

from cli.commands.remove_mods import remove_mods


def test_remove_mods_unknown_mod_raises(manager: Manager) -> None:
    manager.add_game("ut99")

    with pytest.raises(ValueError):
        remove_mods(manager, "ut99", ["nonexistent"])


def test_remove_mods_removes_registered_mod(manager: Manager, tmp_path) -> None:
    manager.add_game("ut99")

    mod_path = tmp_path / "mod-1"
    mod_path.mkdir()

    manager.add_mod("ut99", str(mod_path))
    remove_mods(manager, "ut99", ["mod-1"])

    assert manager.get_mods("ut99") == {}
