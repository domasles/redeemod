import pytest

from backend.manager import Manager


@pytest.fixture
def manager(tmp_path) -> Manager:
    return Manager(storage_file=tmp_path / "settings.json")


def test_empty_state(manager):
    assert manager.get_added_games() == []
    assert manager.get_mods("ut99") == {}
    assert manager.get_custom_paths("ut99") == {}


def test_add_game(manager):
    manager.add_game("ut99")
    assert manager.get_added_games() == ["ut99"]


def test_add_game_is_idempotent(manager):
    manager.add_game("ut99")
    manager.add_game("ut99")

    assert manager.get_added_games() == ["ut99"]


def test_remove_game_cleans_related_data(manager):
    manager.add_game("ut99")
    manager.add_mod("ut99", "/tmp/SuperMod")
    manager.save_custom_paths("ut99", {"executable_path": "/tmp/ut99"})

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


def test_remove_mod(manager):
    manager.add_mod("ut99", "/tmp/SuperMod")
    manager.remove_mod("ut99", "SuperMod")

    assert manager.get_mods("ut99") == {}


def test_remove_unknown_mod_is_noop(manager):
    manager.remove_mod("ut99", "Nope")
    assert manager.get_mods("ut99") == {}


def test_save_custom_paths_per_game(manager):
    manager.save_custom_paths("ut99", {"executable_path": "/a"})
    manager.save_custom_paths("ioq3", {"executable_path": "/b"})

    assert manager.get_custom_paths("ut99") == {"executable_path": "/a"}
    assert manager.get_custom_paths("ioq3") == {"executable_path": "/b"}


def test_persistence_roundtrip(tmp_path):
    storage = tmp_path / "settings.json"

    first = Manager(storage_file=storage)
    first.add_game("ut99")
    first.add_mod("ut99", "/tmp/SuperMod")
    first.save_custom_paths("ut99", {"executable_path": "/tmp/ut99"})

    second = Manager(storage_file=storage)

    assert second.get_added_games() == ["ut99"]
    assert second.get_mods("ut99") == {"SuperMod": "/tmp/SuperMod"}
    assert second.get_custom_paths("ut99") == {"executable_path": "/tmp/ut99"}


def test_load_resets_on_corrupt_file(tmp_path):
    storage = tmp_path / "settings.json"
    storage.write_text("{ not valid json", encoding="utf-8")

    manager = Manager(storage_file=storage)

    assert manager.get_added_games() == []
    assert manager.data == {"games": [], "mods": {}}
