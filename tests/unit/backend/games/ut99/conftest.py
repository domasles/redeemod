from __future__ import annotations

import pytest

from pathlib import Path

from backend.models import GameConfig


@pytest.fixture
def installed_game(tmp_path) -> tuple[Path, Path, Path]:
    """Creates the installed UT99 game: (executable, Game.ini, mod directory)."""

    exe = tmp_path / "game"
    exe.touch()

    ini = tmp_path / "Game.ini"
    ini.write_text("[Core.System]\r\n", encoding="utf-8", newline="")

    mod_dir = tmp_path / "mod" / "MyMod"
    mod_dir.mkdir(parents=True)
    (mod_dir / "Rocket.u").write_text("")

    return exe, ini, mod_dir


@pytest.fixture
def game_config(installed_game) -> GameConfig:
    """GameConfig pointing at the install produced by ``installed_game``."""

    exe, ini, _ = installed_game

    return GameConfig.from_dict(
        {
            "executable_paths": {"linux": [str(exe)], "windows": [str(exe)]},
            "config_paths": {"linux": [str(ini)], "windows": [str(ini)]},
        }
    )
