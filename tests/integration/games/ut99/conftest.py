from __future__ import annotations

import pytest

from pathlib import Path

from backend.models import GameConfig


@pytest.fixture
def installed_game(tmp_path) -> tuple[Path, Path, GameConfig]:
    """Sets up the installed UT99 game."""

    exe = tmp_path / "System" / "game-bin"
    exe.parent.mkdir(parents=True)
    exe.touch()

    ini = tmp_path / "System" / "Game.ini"
    ini.write_text("[Core.System]\r\n", encoding="utf-8", newline="")

    config = GameConfig.from_dict(
        {
            "executable_paths": {"linux": [str(exe)], "windows": [str(exe)]},
            "config_paths": {"linux": [str(ini)], "windows": [str(ini)]},
        }
    )

    return exe, ini, config
