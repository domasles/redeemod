from __future__ import annotations

import pytest


class RecordingLauncher:
    """Records every launch invocation instead of spawning a process."""

    def __init__(self) -> None:
        self.calls: list[tuple[list[str], str | None]] = []

    def __call__(self, cmd: list[str], cwd: str | None = None) -> None:
        self.calls.append((cmd, cwd))


@pytest.fixture
def recording_launcher() -> RecordingLauncher:
    return RecordingLauncher()
