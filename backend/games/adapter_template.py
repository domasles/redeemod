from pathlib import Path

from backend.games.base import BaseGameAdapter


class TemplateAdapter(BaseGameAdapter):
    game_id = "template"
    display_name = "Game Adapter Template"

    def __init__(self, custom_paths: dict[str, str] | None = None, **kwargs):
        super().__init__(custom_paths, **kwargs)

    def build_arguments(self, executable: Path, selected_mod_paths: list[Path]) -> list[str]:
        return []
