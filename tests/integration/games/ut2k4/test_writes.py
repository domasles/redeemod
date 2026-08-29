from backend.games.ut2k4.adapter import UT2K4GameAdapter


def test_build_arguments_writes_mod_files_and_flag(game_install, tmp_path):
    exe, ini, config = game_install

    mod_dir = tmp_path / "Mods" / "SomeMod"
    mod_dir.mkdir(parents=True)
    (mod_dir / "Wep.u").write_text("")

    adapter = UT2K4GameAdapter(config=config)

    cmd = adapter.build_arguments(exe, [mod_dir])
    assert cmd == ["-mod=RedeeMOD"]

    app_mod_dir = tmp_path / "RedeeMOD"

    assert (app_mod_dir / "UT2K4Mod.ini").exists()
    assert (app_mod_dir / "System" / "Default.ini").exists()
    assert (app_mod_dir / "System" / "DefUser.ini").exists()

    default_ini = (app_mod_dir / "System" / "Default.ini").read_text(encoding="utf-8").replace("\\", "/")
    assert "+Paths=../Mods/SomeMod/*.u" in default_ini


def test_music_extension_generates_music_path(game_install, tmp_path):
    exe, ini, config = game_install

    mod_dir = tmp_path / "Mods" / "SomeMod"
    mod_dir.mkdir(parents=True)
    (mod_dir / "Music.ogg").write_text("")

    adapter = UT2K4GameAdapter(config=config)
    adapter.build_arguments(exe, [mod_dir])

    default_ini = (tmp_path / "RedeeMOD" / "System" / "Default.ini").read_text(encoding="utf-8").replace("\\", "/")
    assert "+MusicPath=../Mods/SomeMod" in default_ini


def test_cache_extension_generates_cache_record_path(game_install, tmp_path):
    exe, ini, config = game_install

    mod_dir = tmp_path / "Mods" / "SomeMod"
    mod_dir.mkdir(parents=True)
    (mod_dir / "Cache.ucl").write_text("")

    adapter = UT2K4GameAdapter(config=config)
    adapter.build_arguments(exe, [mod_dir])

    default_ini = (tmp_path / "RedeeMOD" / "System" / "Default.ini").read_text(encoding="utf-8").replace("\\", "/")
    assert "+CacheRecordPath=../Mods/SomeMod/*.ucl" in default_ini


def test_no_matching_files_still_builds_empty_scaffold(game_install, tmp_path):
    exe, ini, config = game_install

    mod_dir = tmp_path / "Mods" / "SomeMod"
    mod_dir.mkdir(parents=True)
    (mod_dir / "readme.txt").write_text("")

    adapter = UT2K4GameAdapter(config=config)

    cmd = adapter.build_arguments(exe, [mod_dir])
    assert cmd == ["-mod=RedeeMOD"]

    default_ini = (tmp_path / "RedeeMOD" / "System" / "Default.ini").read_text(encoding="utf-8").replace("\\", "/")
    assert default_ini == "[Core.System]\n"


def test_build_arguments_regenerates_after_cleanup(game_install, tmp_path):
    exe, ini, config = game_install

    mod_dir = tmp_path / "Mods" / "SomeMod"
    mod_dir.mkdir(parents=True)
    (mod_dir / "Wep.u").write_text("")

    adapter = UT2K4GameAdapter(config=config)

    adapter.build_arguments(exe, [mod_dir])
    first_default = (tmp_path / "RedeeMOD" / "System" / "Default.ini").read_text(encoding="utf-8")

    adapter.build_arguments(exe, [mod_dir])
    second_default = (tmp_path / "RedeeMOD" / "System" / "Default.ini").read_text(encoding="utf-8")

    assert first_default == second_default


def test_cleanup_removes_existing_generated_files(game_install, tmp_path):
    exe, ini, config = game_install

    generated = tmp_path / "RedeeMOD" / "System"
    generated.mkdir(parents=True)
    (generated / "Default.ini").write_text("stale", encoding="utf-8")

    adapter = UT2K4GameAdapter(config=config)
    adapter._cleanup_generated_files()

    assert not (tmp_path / "RedeeMOD").exists()
