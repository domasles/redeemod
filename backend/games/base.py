from abc import ABC, abstractmethod
from pathlib import Path
from typing import List


class BaseGameAdapter(ABC):
    @property
    @abstractmethod
    def game_id(self) -> str:
        """Unique key for the game."""
        pass

    @property
    @abstractmethod
    def display_name(self) -> str:
        """User-friendly name."""
        pass

    @abstractmethod
    def launch(self, selected_mod_paths: List[Path]) -> None:
        """Prepares configuration/INI files and launches the executable."""
        pass
