from __future__ import annotations

import pytest

from backend.games.ioq3.adapter import IOQ3GameAdapter
from backend.models import GameConfig


@pytest.fixture
def adapter() -> IOQ3GameAdapter:
    return IOQ3GameAdapter(config=GameConfig())
