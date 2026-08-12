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
        )


@dataclass
class GameConfig:
    executable_paths: PlatformPaths
    config_paths: PlatformPaths

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GameConfig":
        return cls(
            executable_paths=PlatformPaths.from_dict(data.get("executable_paths", {})),
            config_paths=PlatformPaths.from_dict(data.get("config_paths", {}))
        )


@dataclass
class Config:
    games: Dict[str, GameConfig]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Config":
        games_data = data if isinstance(data, dict) else {}
        return cls(games={game_id: GameConfig.from_dict(cfg) for game_id, cfg in games_data.items()})
