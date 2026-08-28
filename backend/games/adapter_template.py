from pathlib import Path

from backend.games.base import BaseGameAdapter


class TemplateAdapter(BaseGameAdapter):
    @property
    def game_id(self) -> str:
        return "template"

    @property
    def display_name(self) -> str:
        return "Game Adapter Template"

    def __init__(self, custom_paths: dict[str, str] | None = None):
        super().__init__(custom_paths)

    def build_arguments(self, executable: Path, selected_mod_paths: list[Path]) -> list[str]:
        return []
