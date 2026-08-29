from backend.games.ut2k4.adapter import UT2K4GameAdapter
from backend.models import GameConfig


def test_class_level_identity():
    assert UT2K4GameAdapter.game_id == "ut2k4"
    assert UT2K4GameAdapter.display_name == "Unreal Tournament 2004"
    assert UT2K4GameAdapter().allowed_mod_amount is None


def test_extension_sets():
    adapter = UT2K4GameAdapter(config=GameConfig())

    assert {"u", "utx", "usx", "ukx", "uax", "upl"} <= adapter.content_extensions
    assert "ogg" in adapter.music_extensions
    assert "ucl" in adapter.cache_extensions


def test_build_arguments_without_mods_returns_empty(tmp_path, game_config):
    exe = tmp_path / "game"
    exe.touch()

    adapter = UT2K4GameAdapter(config=game_config)

    assert adapter.build_arguments(exe, []) == []
    assert not (tmp_path / "RedeeMOD").exists()
