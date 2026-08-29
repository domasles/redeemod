from backend.models import GameConfig, PlatformPaths


def test_platform_paths_from_dict():
    paths = PlatformPaths.from_dict({"linux": ["/bin/game"], "windows": ["C:\\Game\\game.exe"]})

    assert paths.linux == ["/bin/game"]
    assert paths.windows == ["C:\\Game\\game.exe"]


def test_platform_paths_defaults_to_empty():
    paths = PlatformPaths.from_dict({})

    assert paths.linux == []
    assert paths.windows == []


def test_game_config_from_dict_keeps_platform_dicts():
    config = GameConfig.from_dict(
        {
            "executable_paths": {"linux": ["/bin/game"], "windows": []},
            "config_paths": {"windows": ["C:\\Game\\game.ini"]},
        }
    )

    assert set(config.paths) == {"executable_paths", "config_paths"}


def test_game_config_from_dict_skips_non_dict_values():
    config = GameConfig.from_dict(
        {
            "executable_paths": {"linux": ["/bin/game"], "windows": []},
            "extra": "not a dict",
            "enabled": True,
        }
    )

    assert set(config.paths) == {"executable_paths"}


def test_game_config_defaults():
    config = GameConfig()
    assert config.paths == {}
