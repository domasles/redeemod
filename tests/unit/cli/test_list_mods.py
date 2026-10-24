from backend.manager import Manager

from cli.commands.list_mods import list_mods


def test_list_mods_empty(manager: Manager, capsys) -> None:
    manager.add_game("fake")

    list_mods(manager, "fake")
    captured = capsys.readouterr()

    assert "No added mods found." in captured.out


def test_list_mods_lists_added_mods(manager: Manager, tmp_path, capsys) -> None:
    manager.add_game("fake")

    mod_path = tmp_path / "mod-1"
    mod_path.mkdir()

    manager.add_mod("fake", str(mod_path))
    list_mods(manager, "fake")

    captured = capsys.readouterr()
    assert "mod-1" in captured.out
