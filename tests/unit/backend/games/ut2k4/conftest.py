from __future__ import annotations

import pytest

from backend.models import GameConfig


@pytest.fixture
def game_config(tmp_path) -> GameConfig:
    """GameConfig pointing at an executable inside ``tmp_path``."""

    executable = str(tmp_path / "game")
    return GameConfig.from_dict({"executable_paths": {"linux": [executable], "windows": [executable]}})
