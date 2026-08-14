import subprocess

from typing import List, Dict, Optional
from pathlib import Path

from backend.utils.filesystem import expand_path, get_base_directory, get_project_directory, get_relative_path
from backend.discovery import discover_installation, load_config
from backend.utils.ini import append_to_ini_file
from backend.games.base import BaseGameAdapter
from backend.constants import *


class UT99GameAdapter(BaseGameAdapter):
    @property
    def game_id(self) -> str:
        return "ut99"

    @property
    def display_name(self) -> str:
        return "Unreal Tournament '99"

    def __init__(self, custom_paths: Optional[Dict[str, str]] = None):
        config_file = get_project_directory() / "backend/config/config.json"

        self.config = load_config(config_file)
        self.content_exts = ["u", "unr", "utx", "uax", "umx"]
        self.loc_exts = ["int", "det", "frt", "est", "itt", "rut"]

        custom_paths = custom_paths or {}

        self.executable_path = expand_path(custom_paths["executable_path"]) if custom_paths.get("executable_path") else None
        self.config_path = expand_path(custom_paths["config_path"]) if custom_paths.get("config_path") else None

        game_cfg = self.config.games.get(self.game_id)

        if game_cfg:
            auto_exe, auto_cfg = discover_installation(game_cfg)

            if not self.executable_path:
                self.executable_path = auto_exe

            if not self.config_path:
                self.config_path = auto_cfg

    def launch(self, selected_mod_paths: List[Path]) -> None:
        if not self.executable_path or not self.executable_path.exists():
            raise FileNotFoundError("UT99 installation not found.")

        cmd = [str(self.executable_path)]

        if selected_mod_paths and self.config_path and self.config_path.exists():
            mod_ini_path = get_relative_path(get_base_directory(self.executable_path), self._apply_mods_to_ini(selected_mod_paths))
            cmd.append(f"INI={mod_ini_path}")

        subprocess.Popen(cmd, cwd=str(get_base_directory(self.executable_path)))

    def scan_mod_directory(self, target_dir: Path) -> List[tuple[Path, str]]:
        target_dir = expand_path(target_dir)
        mod_files = []

        if not target_dir.exists():
            return mod_files

        for item in target_dir.rglob("*"):
            if not item.is_file():
                continue

            ext = item.suffix.lstrip(".").lower()

            if ext in self.content_exts or ext in self.loc_exts:
                mod_files.append((item, ext))

        return mod_files

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

                if ext in self.content_exts:
                    path_entries.add(f"Paths={rel_dir}/*.{ext}")

                elif ext in self.loc_exts:
                    lang_entries.add(f"LangPaths={rel_dir}/*.<lang>")

        new_content = "\n".join(sorted(path_entries | lang_entries)) + "\n"

        mod_ini_path = get_base_directory(self.config_path) / CONFIG_FILE_NAME
        mod_ini_path.parent.mkdir(parents=True, exist_ok=True)

        if new_content.strip():
            updated_ini = append_to_ini_file(self.config_path, "Core.System", new_content)
            mod_ini_path.write_text(updated_ini, "utf-8")

        return mod_ini_path
