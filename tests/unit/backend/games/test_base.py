import pytest

from pathlib import Path

from backend.games.base import BaseGameAdapter
from backend.models import GameConfig


class _StubAdapter(BaseGameAdapter):
    game_id = "stub"
    display_name = "Stub Game"

    @property
    def file_extensions(self) -> set[str]:
        return {"u", "umx"}

    def build_arguments(self, executable: Path, selected_mod_paths: list[Path]) -> list[str]:
        return []


def _config(**path_groups: list[str]) -> GameConfig:
    return GameConfig.from_dict({key: {"linux": values, "windows": values} for key, values in path_groups.items()})


@pytest.mark.parametrize(
    "attrs",
    [
        {"display_name": "Stub Game"},
        {"game_id": "stub"},
        {"game_id": "stub", "display_name": "   "},
        {"game_id": 1, "display_name": "Stub Game"},
    ],
)
def test_subclass_requires_identity(attrs):
    with pytest.raises(TypeError):
        type("InvalidAdapter", (BaseGameAdapter,), attrs)


def test_injected_config_is_used(tmp_path):
    exe = tmp_path / "game"
    exe.touch()

    adapter = _StubAdapter(config=_config(executable_paths=[str(exe)]))

    assert adapter.resolved_path("executable_path") == exe
    assert adapter.required_path_keys == ["executable_path"]


def test_required_path_keys_derived_from_config(tmp_path):
    exe = tmp_path / "game"
    exe.touch()

    adapter = _StubAdapter(config=_config(executable_paths=[str(exe)], config_paths=[str(tmp_path / "Game.ini")]))
    assert adapter.required_path_keys == ["executable_path", "config_path"]


def test_get_missing_paths(tmp_path):
    exe = tmp_path / "game"
    exe.touch()

    adapter = _StubAdapter(config=_config(executable_paths=[str(exe)], config_paths=[str(tmp_path / "missing.ini")]))
    assert adapter.get_missing_paths() == ["config_path"]


def test_get_missing_paths_empty_when_all_present(tmp_path):
    exe = tmp_path / "game"
    exe.touch()
    ini = tmp_path / "Game.ini"
    ini.write_text("", encoding="utf-8")

    adapter = _StubAdapter(config=_config(executable_paths=[str(exe)], config_paths=[str(ini)]))
    assert adapter.get_missing_paths() == []


def test_scan_mod_directory_filters_by_extensions(tmp_path):
    mod_dir = tmp_path / "mod"
    (mod_dir / "deep").mkdir(parents=True)
    (mod_dir / "Rocket.u").write_text("")
    (mod_dir / "desktop.ini").write_text("")
    (mod_dir / "deep" / "Sound.umx").write_text("")

    adapter = _StubAdapter(config=_config())

    results = adapter.scan_mod_directory(mod_dir)
    kinds = {ext for _, ext in results}

    assert "u" in kinds
    assert "umx" in kinds
    assert "ini" not in kinds


def test_scan_mod_directory_missing_dir_returns_empty(tmp_path):
    adapter = _StubAdapter(config=_config())
    assert adapter.scan_mod_directory(tmp_path / "nope") == []


def test_launch_uses_injected_process_launcher(tmp_path, recording_launcher):
    exe = tmp_path / "game"
    exe.touch()

    adapter = _StubAdapter(config=_config(executable_paths=[str(exe)]), process_launcher=recording_launcher)
    adapter.launch([])

    assert recording_launcher.calls == [([str(exe)], str(exe.parent))]


def test_launch_raises_when_executable_missing(tmp_path, recording_launcher):
    adapter = _StubAdapter(
        config=_config(executable_paths=[str(tmp_path / "missing")]),
        process_launcher=recording_launcher,
    )

    with pytest.raises(FileNotFoundError):
        adapter.launch([])

    assert recording_launcher.calls == []
