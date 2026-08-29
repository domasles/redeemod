from __future__ import annotations

import pytest

from pathlib import Path

from backend.models import GameConfig


@pytest.fixture
def game_install(tmp_path) -> tuple[Path, Path, GameConfig]:
    """Sets up the installed UT2004 game."""

    exe = tmp_path / "System" / "game-bin"
    exe.parent.mkdir(parents=True)
    exe.touch()

    ini = tmp_path / "System" / "Game.ini"
    ini.write_text("", encoding="utf-8")

    config = GameConfig.from_dict(
        {
            "executable_paths": {"linux": [str(exe)], "windows": [str(exe)]},
            "config_paths": {"linux": [str(ini)], "windows": [str(ini)]},
        }
    )

    return exe, ini, config
