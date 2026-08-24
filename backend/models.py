from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PlatformPaths:
    linux: list[str] = field(default_factory=list)
    windows: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PlatformPaths:
        return cls(
            linux=data.get("linux", []),
            windows=data.get("windows", [])
        )  # fmt: skip


@dataclass
class GameConfig:
    paths: dict[str, PlatformPaths] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GameConfig:
        paths = {
            key: PlatformPaths.from_dict(val)
            for key, val in data.items()
            if isinstance(val, dict)
        }  # fmt: skip

        return cls(paths=paths)


@dataclass
class Config:
    games: dict[str, GameConfig]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Config:
        return cls(games={game_id: GameConfig.from_dict(cfg) for game_id, cfg in data.items() if isinstance(cfg, dict)})
