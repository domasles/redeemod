from backend.games.ut99.adapter import UT99GameAdapter


def test_class_level_identity():
    assert UT99GameAdapter.game_id == "ut99"
    assert UT99GameAdapter.display_name == "Unreal Tournament '99"


def test_build_arguments_without_mods_returns_empty(installed_game, game_config):
    exe, _, _ = installed_game

    adapter = UT99GameAdapter(config=game_config)
    assert adapter.build_arguments(exe, []) == []


def test_build_arguments_with_mods_adds_ini_flag(installed_game, game_config):
    exe, _, mod_dir = installed_game

    adapter = UT99GameAdapter(config=game_config)
    cmd = adapter.build_arguments(exe, [mod_dir])

    assert cmd == ["INI=RedeeMOD.ini"]


def test_launch_forwards_mod_ini_flag(installed_game, game_config, recording_launcher):
    exe, _, mod_dir = installed_game

    adapter = UT99GameAdapter(config=game_config, process_launcher=recording_launcher)
    adapter.launch([mod_dir])

    command, cwd = recording_launcher.calls[0]

    assert command == [str(exe), "INI=RedeeMOD.ini"]
    assert cwd == str(exe.parent)
