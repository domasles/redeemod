from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class PlatformPaths:
    linux: List[str] = field(default_factory=list)
    windows: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PlatformPaths":
        return cls(
            linux=data.get("linux", []),
            windows=data.get("windows", [])
        )  # fmt: skip


@dataclass
class GameConfig:
    paths: Dict[str, PlatformPaths] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GameConfig":
        paths = {
            key: PlatformPaths.from_dict(val)
            for key, val in data.items()
            if isinstance(val, dict)
        }  # fmt: skip

        return cls(paths=paths)


@dataclass
class Config:
    games: Dict[str, GameConfig]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Config":
        games_data = data if isinstance(data, dict) else {}
        return cls(games={game_id: GameConfig.from_dict(cfg) for game_id, cfg in games_data.items()})
