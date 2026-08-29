import pytest

from backend.games.unrgold.ini import prepend_to_ini_section


def test_inserts_new_content_under_section(tmp_path):
    ini = tmp_path / "game.ini"
    ini.write_text(
        "[Engine.Engine]\r\nSettings=1\r\n[Core.System]\r\nPaths=Existing\r\n[Foo]\r\n",
        encoding="utf-8",
        newline="",
    )

    result = prepend_to_ini_section(ini, "Core.System", "Paths=New")
    assert result == "[Engine.Engine]\nSettings=1\n[Core.System]\nPaths=New\nPaths=Existing\n[Foo]\n"


def test_section_match_is_case_insensitive(tmp_path):
    ini = tmp_path / "game.ini"
    ini.write_text("[core.system]\r\nX=1\r\n", encoding="utf-8", newline="")

    result = prepend_to_ini_section(ini, "Core.System", "Paths=A")
    assert result == "[core.system]\nPaths=A\nX=1\n"


def test_missing_section_raises(tmp_path):
    ini = tmp_path / "game.ini"
    ini.write_text("[Other]\r\n", encoding="utf-8", newline="")

    with pytest.raises(ValueError):
        prepend_to_ini_section(ini, "Core.System", "Paths=A")


def test_crlf_input_is_normalized_to_lf(tmp_path):
    ini = tmp_path / "game.ini"
    ini.write_text("[Core.System]\r\nPaths=Existing\r\n", encoding="utf-8", newline="")

    result = prepend_to_ini_section(ini, "Core.System", "Paths=New")
    assert result == "[Core.System]\nPaths=New\nPaths=Existing\n"


def test_prior_content_in_section_is_preserved_below_new(tmp_path):
    ini = tmp_path / "game.ini"
    ini.write_text("[Core.System]\r\nLangPaths=Old\r\nPaths=OldToo\r\n", encoding="utf-8", newline="")

    result = prepend_to_ini_section(ini, "Core.System", "Paths=New")
    assert result == "[Core.System]\nPaths=New\nLangPaths=Old\nPaths=OldToo\n"


def test_new_content_is_stripped_of_whitespace(tmp_path):
    ini = tmp_path / "game.ini"
    ini.write_text("[Core.System]\r\n", encoding="utf-8", newline="")

    result = prepend_to_ini_section(ini, "Core.System", "  Paths=New  \n")
    assert result == "[Core.System]\nPaths=New\n"


def test_section_at_end_of_file_without_trailing_newline(tmp_path):
    ini = tmp_path / "game.ini"
    ini.write_text("[Foo]\r\n[Core.System]", encoding="utf-8", newline="")

    result = prepend_to_ini_section(ini, "Core.System", "Paths=New")
    assert result == "[Foo]\n[Core.System]\nPaths=New\n"


def test_only_first_occurrence_of_section_is_modified(tmp_path):
    ini = tmp_path / "game.ini"
    ini.write_text("[Core.System]\r\nPaths=A\r\n[Other]\r\n[Core.System]\r\nPaths=B\r\n", encoding="utf-8", newline="")

    result = prepend_to_ini_section(ini, "Core.System", "Paths=New")
    assert result == "[Core.System]\nPaths=New\nPaths=A\n[Other]\n[Core.System]\nPaths=B\n"
