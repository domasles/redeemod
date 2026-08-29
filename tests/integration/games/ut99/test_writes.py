from backend.games.ut99.adapter import UT99GameAdapter


def test_content_extension_adds_path_entry(installed_game, tmp_path):
    exe, ini, config = installed_game

    mod_dir = tmp_path / "Mods" / "MyMod"
    mod_dir.mkdir(parents=True)
    (mod_dir / "Rocket.umx").write_text("")

    adapter = UT99GameAdapter(config=config)
    mod_ini_path = adapter._apply_mods_to_ini([mod_dir], exe.parent, ini)

    content = mod_ini_path.read_text(encoding="utf-8").replace("\\", "/")

    assert mod_ini_path == tmp_path / "System" / "RedeeMOD.ini"
    assert content == "[Core.System]\nPaths=../Mods/MyMod/*.umx\n"


def test_locale_extension_adds_langpath_entry(installed_game, tmp_path):
    exe, ini, config = installed_game

    mod_dir = tmp_path / "Mods" / "MyMod"
    mod_dir.mkdir(parents=True)
    (mod_dir / "Menu.int").write_text("")

    adapter = UT99GameAdapter(config=config)
    mod_ini_path = adapter._apply_mods_to_ini([mod_dir], exe.parent, ini)

    content = mod_ini_path.read_text(encoding="utf-8").replace("\\", "/")
    assert content == "[Core.System]\nLangPaths=../Mods/MyMod/*.<lang>\n"


def test_content_and_locale_entries_are_sorted(installed_game, tmp_path):
    exe, ini, config = installed_game

    mod_dir = tmp_path / "Mods" / "MyMod"
    mod_dir.mkdir(parents=True)
    (mod_dir / "Guns.u").write_text("")
    (mod_dir / "Menu.int").write_text("")

    adapter = UT99GameAdapter(config=config)
    mod_ini_path = adapter._apply_mods_to_ini([mod_dir], exe.parent, ini)

    content = mod_ini_path.read_text(encoding="utf-8").replace("\\", "/")
    assert content == "[Core.System]\nLangPaths=../Mods/MyMod/*.<lang>\nPaths=../Mods/MyMod/*.u\n"


def test_nested_files_use_their_own_relative_dir(installed_game, tmp_path):
    exe, ini, config = installed_game

    mod_dir = tmp_path / "Mods" / "MyMod"
    nested = mod_dir / "sub"
    nested.mkdir(parents=True)
    (nested / "Level.utx").write_text("")

    adapter = UT99GameAdapter(config=config)
    mod_ini_path = adapter._apply_mods_to_ini([mod_dir], exe.parent, ini)

    content = mod_ini_path.read_text(encoding="utf-8").replace("\\", "/")
    assert content == "[Core.System]\nPaths=../Mods/MyMod/sub/*.utx\n"


def test_multiple_mods_produce_distinct_entries(installed_game, tmp_path):
    exe, ini, config = installed_game

    first = tmp_path / "Mods" / "First"
    first.mkdir(parents=True)
    (first / "Guns.u").write_text("")

    second = tmp_path / "Mods" / "Second"
    second.mkdir(parents=True)
    (second / "Menu.int").write_text("")

    adapter = UT99GameAdapter(config=config)
    mod_ini_path = adapter._apply_mods_to_ini([first, second], exe.parent, ini)

    content = mod_ini_path.read_text(encoding="utf-8").replace("\\", "/")
    assert content == ("[Core.System]\n" "LangPaths=../Mods/Second/*.<lang>\n" "Paths=../Mods/First/*.u\n")


def test_no_matching_files_writes_no_ini(installed_game, tmp_path):
    exe, ini, config = installed_game

    mod_dir = tmp_path / "Mods" / "MyMod"
    mod_dir.mkdir(parents=True)
    (mod_dir / "readme.txt").write_text("")

    adapter = UT99GameAdapter(config=config)
    adapter._apply_mods_to_ini([mod_dir], exe.parent, ini)

    assert not (tmp_path / "System" / "RedeeMOD.ini").exists()
