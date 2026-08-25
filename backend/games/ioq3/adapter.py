import subprocess

from pathlib import Path

from backend.utils.filesystem import get_base_directory
from backend.games.base import BaseGameAdapter


class IOQ3GameAdapter(BaseGameAdapter):
    @property
    def game_id(self) -> str:
        return "ioq3"

    @property
    def display_name(self) -> str:
        return "IOQuake 3"

    @property
    def logo(self) -> Path | None:
        return self.adapter_assets_path / "logo.svg"

    @property
    def allowed_mod_amount(self):
        return 1

    @property
    def file_extensions(self) -> set[str]:
        return self.content_extensions

    def __init__(self, custom_paths: dict[str, str] | None = None):
        super().__init__(custom_paths)
        self.content_extensions = {"pk3"}

    def launch(self, selected_mod_paths: list[Path]):
        if not self.executable_path or not self.executable_path.exists():
            raise FileNotFoundError(f"{self.display_name} installation not found.")

        cmd = [str(self.executable_path)]

        if selected_mod_paths:
            for item, _ext in self.scan_mod_directory(selected_mod_paths[0]):
                if get_base_directory(item) != selected_mod_paths[0]:
                    raise FileNotFoundError(f"All .pk3 files must be under the selected mod's root.")

            cmd.append("+set")
            cmd.append("fs_steampath")
            cmd.append(f"{get_base_directory(selected_mod_paths[0])}")
            cmd.append("+set")
            cmd.append("fs_game")
            cmd.append(f"{selected_mod_paths[0].name}")

        subprocess.Popen(cmd, cwd=str(get_base_directory(self.executable_path)))
