import zipfile
import pytest

from pathlib import Path

from backend.games.ioq3.adapter import IOQ3GameAdapter
from backend.games.ioq3.checksum import calculate_archive_adler32


def _make_pk3(path: Path, files: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(path, "w") as zf:
        for name, data in files.items():
            zf.writestr(name, data)


def test_class_level_identity():
    assert IOQ3GameAdapter.game_id == "ioq3"
    assert IOQ3GameAdapter.display_name == "IOQuake 3"
    assert IOQ3GameAdapter().allowed_mod_amount == 1


def test_analyze_mod_classifies_standalone(tmp_path, adapter):
    mod_dir = tmp_path / "MyMod"
    _make_pk3(mod_dir / "mod.pk3", {"default.cfg": 'seta fs_game ""\n'})

    profile = adapter._analyze_mod(mod_dir)

    assert profile.is_standalone
    assert not profile.is_missionpack


def test_analyze_mod_classifies_plain_mod(tmp_path, adapter):
    mod_dir = tmp_path / "MyMod"
    _make_pk3(mod_dir / "mod.pk3", {"scripts/foo.cfg": "// data\n"})

    profile = adapter._analyze_mod(mod_dir)

    assert not profile.is_standalone
    assert not profile.is_missionpack


def test_analyze_mod_rejects_nested_pk3(tmp_path, adapter):
    mod_dir = tmp_path / "MyMod"
    _make_pk3(mod_dir / "sub" / "a.pk3", {"x.txt": "data"})

    with pytest.raises(FileNotFoundError):
        adapter._analyze_mod(mod_dir)


def test_team_arena_classifies_missionpack(tmp_path, monkeypatch, adapter):
    mod_dir = tmp_path / "missionpack"
    pk3 = mod_dir / "mp.pk3"

    _make_pk3(pk3, {"scripts/mp.cfg": "// team arena\n"})
    monkeypatch.setattr("backend.games.ioq3.adapter.TEAM_ARENA_CHECKSUMS", {calculate_archive_adler32(pk3)})

    profile = adapter._analyze_mod(mod_dir)
    assert profile.is_missionpack


def test_team_arena_requires_missionpack_folder(tmp_path, monkeypatch, adapter):
    mod_dir = tmp_path / "wrong_name"
    pk3 = mod_dir / "mp.pk3"

    _make_pk3(pk3, {"scripts/mp.cfg": "// team arena\n"})
    monkeypatch.setattr("backend.games.ioq3.adapter.TEAM_ARENA_CHECKSUMS", {calculate_archive_adler32(pk3)})

    with pytest.raises(ValueError):
        adapter._analyze_mod(mod_dir)


def test_quake3_assets_rejected(tmp_path, monkeypatch, adapter):
    mod_dir = tmp_path / "MyMod"
    pk3 = mod_dir / "pak0.pk3"

    _make_pk3(pk3, {"a.txt": "data\n"})
    monkeypatch.setattr("backend.games.ioq3.adapter.QUAKE_3_CHECKSUMS", {calculate_archive_adler32(pk3)})

    with pytest.raises(ValueError):
        adapter._analyze_mod(mod_dir)


def test_build_arguments_standalone_uses_com_basegame(tmp_path, adapter):
    exe = tmp_path / "ioquake3"
    exe.touch()

    mod_dir = tmp_path / "MyMod"
    _make_pk3(mod_dir / "mod.pk3", {"default.cfg": "x\n"})

    cmd = adapter.build_arguments(exe, [mod_dir])
    assert cmd == ["+set", "fs_steampath", str(tmp_path), "+set", "com_basegame", "MyMod"]


def test_build_arguments_non_standalone_uses_fs_game(tmp_path, monkeypatch, adapter):
    exe = tmp_path / "bin" / "ioquake3"
    exe.parent.mkdir(parents=True)
    exe.touch()

    baseq3 = exe.parent / "baseq3"
    baseq3.mkdir()

    quake_pk3 = baseq3 / "pak0.pk3"
    _make_pk3(quake_pk3, {"a.txt": "data\n"})

    monkeypatch.setattr(
        "backend.games.ioq3.adapter.QUAKE_3_CHECKSUMS",
        {calculate_archive_adler32(quake_pk3)},
    )

    mod_dir = tmp_path / "MyMod"
    _make_pk3(mod_dir / "mod.pk3", {"b.txt": "data\n"})

    cmd = adapter.build_arguments(exe, [mod_dir])
    assert cmd == ["+set", "fs_steampath", str(tmp_path), "+set", "fs_game", "MyMod"]


def test_build_arguments_non_standalone_without_quake3_raises(tmp_path, adapter):
    exe = tmp_path / "ioquake3"
    exe.touch()

    mod_dir = tmp_path / "MyMod"
    _make_pk3(mod_dir / "mod.pk3", {"b.txt": "data\n"})

    with pytest.raises(ValueError):
        adapter.build_arguments(exe, [mod_dir])


def test_build_arguments_standalone_without_quake3_raises(tmp_path, adapter):
    exe = tmp_path / "ioquake3"
    exe.touch()

    with pytest.raises(FileNotFoundError):
        adapter.build_arguments(exe, [])
