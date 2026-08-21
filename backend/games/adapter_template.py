import subprocess

from typing import List, Dict
from pathlib import Path

from backend.games.base import BaseGameAdapter
from backend.constants import *


class TemplateAdapter(BaseGameAdapter):
    @property
    def game_id(self) -> str:
        return "template"

    @property
    def display_name(self) -> str:
        return "Game Adapter Template"

    def __init__(self, custom_paths: Dict[str, str] | None = None):
        super().__init__(custom_paths)

    def launch(self, selected_mod_paths: List[Path]) -> None:
        print(f"Launching {self.display_name}!")
