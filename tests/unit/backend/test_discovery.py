from pathlib import Path

from backend.discovery import discover_all_paths, discover_installation
from backend.models import GameConfig


def _config(paths: dict[str, dict[str, list[str]]]) -> GameConfig:
    return GameConfig.from_dict(paths)


def test_platform_selection_isolates_branches():
    config = _config(
        {
            "executable_paths": {"linux": ["/usr/bin/game"], "windows": ["C:\\Game\\game.exe"]},
            "config_paths": {"linux": ["/etc/game.ini"], "windows": []},
        }
    )

    linux = discover_all_paths(config, platform_key="linux")
    windows = discover_all_paths(config, platform_key="windows")

    assert linux["executable_paths"] == [Path("/usr/bin/game")]
    assert linux["config_paths"] == [Path("/etc/game.ini")]

    assert windows["executable_paths"] == [Path("C:\\Game\\game.exe")]
    assert windows["config_paths"] == []


def test_custom_path_entry_prepends_to_existing_group(tmp_path):
    config = _config({"executable_paths": {"linux": [str(tmp_path / "default")], "windows": []}})

    discovered = discover_all_paths(
        config,
        custom_paths={"executable_path": str(tmp_path / "custom")},
        platform_key="linux",
    )

    candidates = discovered["executable_paths"]

    assert candidates[0] == tmp_path / "custom"
    assert candidates[1] == tmp_path / "default"


def test_custom_path_entry_creates_new_group(tmp_path):
    config = _config({"executable_paths": {"linux": [str(tmp_path / "game")], "windows": []}})

    discovered = discover_all_paths(
        config,
        custom_paths={"extra_path": str(tmp_path / "extra")},
        platform_key="linux",
    )

    assert discovered["extra_paths"] == [tmp_path / "extra"]


def test_custom_path_duplicate_is_not_readded(tmp_path):
    config = _config({"executable_paths": {"linux": [str(tmp_path / "game")], "windows": []}})

    discovered = discover_all_paths(
        config,
        custom_paths={"executable_path": str(tmp_path / "game")},
        platform_key="linux",
    )

    assert discovered["executable_paths"] == [tmp_path / "game"]


def test_discover_installation_picks_first_existing(tmp_path):
    existing = tmp_path / "existing"
    existing.mkdir()

    config = _config({"executable_paths": {"linux": [str(tmp_path / "missing"), str(existing)], "windows": []}})
    resolved = discover_installation(config, platform_key="linux")

    assert resolved["executable_path"] == existing.resolve()


def test_discover_installation_falls_back_to_first_candidate(tmp_path):
    missing = tmp_path / "missing"
    config = _config({"executable_paths": {"linux": [str(missing)], "windows": []}})
    resolved = discover_installation(config, platform_key="linux")

    assert resolved["executable_path"] == missing.resolve()


def test_discover_installation_returns_none_for_empty_group():
    config = _config({"executable_paths": {"linux": [], "windows": []}})
    resolved = discover_installation(config, platform_key="linux")

    assert resolved["executable_path"] is None


def test_discover_installation_custom_path_wins(tmp_path):
    default = tmp_path / "default"
    default.mkdir()

    custom = tmp_path / "custom"
    custom.mkdir()

    config = _config({"executable_paths": {"linux": [str(default)], "windows": []}})

    resolved = discover_installation(
        config,
        custom_paths={"executable_path": str(custom)},
        platform_key="linux",
    )

    assert resolved["executable_path"] == custom
