from backend.models import GameConfig


def test_game_config_from_dict_skips_non_dict_values():
    config = GameConfig.from_dict(
        {
            "executable_paths": {"linux": ["/bin/game"], "windows": []},
            "extra": "not a dict",
            "enabled": True,
        }
    )

    assert set(config.paths) == {"executable_paths"}
