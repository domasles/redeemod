import pytest

from backend.manager import Manager


@pytest.fixture
def manager(tmp_path) -> Manager:
    return Manager(storage_file=tmp_path / "settings.json")


@pytest.fixture
def mod_dir(manager) -> str:
    mod_path = manager.storage_file.parent / "SuperMod"
    mod_path.mkdir()

    return str(mod_path)


@pytest.fixture
def exe_path(manager) -> str:
    exe = manager.storage_file.parent / "game-bin"
    exe.touch()

    return str(exe)


def test_add_game_is_idempotent(manager):
    manager.add_game("ut99")
    manager.add_game("ut99")

    assert manager.get_added_games() == ["ut99"]


def test_remove_game_cleans_related_data(manager, mod_dir, exe_path):
    manager.add_game("ut99")
    manager.add_mod("ut99", mod_dir)
    manager.save_custom_paths("ut99", {"executable_path": exe_path})

    manager.remove_game("ut99")

    assert manager.get_added_games() == []
    assert manager.get_mods("ut99") == {}
    assert manager.get_custom_paths("ut99") == {}


def test_add_mod_uses_directory_name(tmp_path):
    mod_dir = tmp_path / "SuperMod"
    mod_dir.mkdir()

    manager = Manager(storage_file=tmp_path / "settings.json")
    name = manager.add_mod("ut99", str(mod_dir))

    assert name == "SuperMod"
    assert manager.get_mods("ut99") == {"SuperMod": str(mod_dir)}


def test_remove_mod(manager, mod_dir):
    manager.add_mod("ut99", mod_dir)
    manager.remove_mod("ut99", "SuperMod")

    assert manager.get_mods("ut99") == {}


def test_remove_unknown_mod_is_noop(manager):
    manager.remove_mod("ut99", "Nope")
    assert manager.get_mods("ut99") == {}


def test_persistence_roundtrip(tmp_path):
    storage = tmp_path / "settings.json"

    mod_path = tmp_path / "SuperMod"
    mod_path.mkdir()

    exe = tmp_path / "game-bin"
    exe.touch()

    first = Manager(storage_file=storage)
    first.add_game("ut99")
    first.add_mod("ut99", str(mod_path))
    first.save_custom_paths("ut99", {"executable_path": str(exe)})

    second = Manager(storage_file=storage)

    assert second.get_added_games() == ["ut99"]
    assert second.get_mods("ut99") == {"SuperMod": str(mod_path)}
    assert second.get_custom_paths("ut99") == {"executable_path": str(exe)}


def test_load_resets_on_corrupt_file(tmp_path):
    storage = tmp_path / "settings.json"
    storage.write_text("{ not valid json", encoding="utf-8")

    manager = Manager(storage_file=storage)

    assert manager.get_added_games() == []
    assert manager.data == {"games": [], "mods": {}}
