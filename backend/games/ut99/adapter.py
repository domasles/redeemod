import subprocess

from typing import List, Dict
from pathlib import Path

from backend.utils.filesystem import get_base_directory, get_relative_path
from backend.games.ut99.ini import append_to_ini_file
from backend.games.base import BaseGameAdapter
from backend.constants import *


class UT99GameAdapter(BaseGameAdapter):
    @property
    def game_id(self) -> str:
        return "ut99"

    @property
    def display_name(self) -> str:
        return "Unreal Tournament '99"

    @property
    def logo(self) -> Path | None:
        return self.adapter_assets_path / "logo.png"

    @property
    def file_extensions(self) -> set[str]:
        return self.all_extensions

    def __init__(self, custom_paths: Dict[str, str] | None = None):
        self.content_extensions = {"u", "unr", "utx", "uax", "umx"}
        self.locale_extensions = {"int", "det", "frt", "est", "itt", "rut"}
        self.all_extensions = self.content_extensions | self.locale_extensions

        super().__init__(custom_paths)

    def launch(self, selected_mod_paths: List[Path]) -> None:
        if not self.executable_path or not self.executable_path.exists():
            raise FileNotFoundError("UT99 installation not found.")

        cmd = [str(self.executable_path)]

        if selected_mod_paths and self.config_path and self.config_path.exists():
            mod_ini_path = get_relative_path(get_base_directory(self.executable_path), self._apply_mods_to_ini(selected_mod_paths))
            cmd.append(f"INI={mod_ini_path}")

        subprocess.Popen(cmd, cwd=str(get_base_directory(self.executable_path)))

    def _apply_mods_to_ini(self, mod_paths: List[Path]) -> Path:
        exe_base = get_base_directory(self.executable_path)

        path_entries: set[str] = set()
        lang_entries: set[str] = set()

        for target_dir in mod_paths:
            for item, ext in self.scan_mod_directory(target_dir):
                try:
                    rel_dir = get_relative_path(exe_base, item.parent)

                except ValueError:
                    rel_dir = item.parent

                if ext in self.content_extensions:
                    path_entries.add(f"Paths={rel_dir}/*.{ext}")

                elif ext in self.locale_extensions:
                    lang_entries.add(f"LangPaths={rel_dir}/*.<lang>")

        new_content = "\n".join(sorted(path_entries | lang_entries)) + "\n"

        mod_ini_path = get_base_directory(self.config_path) / f"{APP_NAME}.ini"
        mod_ini_path.parent.mkdir(parents=True, exist_ok=True)

        if new_content.strip():
            updated_ini = append_to_ini_file(self.config_path, "Core.System", new_content)
            mod_ini_path.write_text(updated_ini, "utf-8")

        return mod_ini_path
