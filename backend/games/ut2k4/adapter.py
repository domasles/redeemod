import subprocess
import shutil

from typing import List, Dict, Optional
from pathlib import Path

from backend.utils.filesystem import get_base_directory, get_relative_path
from backend.games.base import BaseGameAdapter
from backend.constants import *


class UT2K4GameAdapter(BaseGameAdapter):
    @property
    def game_id(self) -> str:
        return "ut2k4"

    @property
    def display_name(self) -> str:
        return "Unreal Tournament 2004"

    @property
    def file_extensions(self) -> set[str]:
        return self.all_extensions

    def __init__(self, custom_paths: Optional[Dict[str, str]] = None):
        self.content_extensions = {"u", "ut2", "utx", "usx", "ukx", "uax"}
        self.music_extensions = {"ogg"}
        self.cache_extensions = {"ucl"}
        self.all_extensions = self.content_extensions | self.music_extensions | self.cache_extensions

        super().__init__(custom_paths)

    def launch(self, selected_mod_paths: List[Path]) -> None:
        if not self.executable_path or not self.executable_path.exists():
            raise FileNotFoundError("UT2K4 installation not found.")

        cmd = [str(self.executable_path)]

        if selected_mod_paths and self.config_path and self.config_path.exists():
            self._cleanup_generated_files()
            self._write_mod_files(selected_mod_paths)

            cmd.append(f"-mod={APP_NAME}")

        subprocess.Popen(cmd, cwd=str(get_base_directory(self.executable_path)))

    def _cleanup_generated_files(self) -> None:
        candidate_config_paths = self.all_configured_data.get("config_paths", [])
        cleaned_dirs = set()

        for cfg_path in candidate_config_paths:
            if not cfg_path:
                continue

            target_app_dir = get_base_directory(cfg_path).parent / APP_NAME

            if target_app_dir not in cleaned_dirs:
                cleaned_dirs.add(target_app_dir)

                if target_app_dir.exists():
                    shutil.rmtree(target_app_dir)

    def _write_mod_files(self, mod_paths: List[Path]) -> None:
        exe_base = get_base_directory(self.executable_path)
        install_dir = exe_base.parent
        app_mod_dir = install_dir / APP_NAME
        app_sys_dir = app_mod_dir / "System"

        app_sys_dir.mkdir(parents=True, exist_ok=True)

        ut2k4mod_content = (
            "[MOD]\r\n"
            'ModTitle="RedeeMOD"\r\n'
            'ModDesc="A package of selected mods through RedeeMOD launcher."\r\n'
        )

        default_ini_content = self._generate_default_ini(mod_paths, exe_base)

        (app_mod_dir / "UT2K4Mod.ini").write_bytes(ut2k4mod_content.encode("utf-8"))
        (app_sys_dir / "Default.ini").write_bytes(default_ini_content.encode("utf-8"))
        (app_sys_dir / "DefUser.ini").write_bytes("\r\n".encode("utf-8"))

    def _generate_default_ini(self, mod_paths: List[Path], exe_base: Path) -> str:
        cache_entries: set[str] = set()
        music_entries: set[str] = set()
        path_entries: set[str] = set()

        for target_dir in mod_paths:
            for item, ext in self.scan_mod_directory(target_dir):
                try:
                    rel_dir = get_relative_path(exe_base, item.parent)

                except ValueError:
                    rel_dir = item.parent

                if ext in self.cache_extensions:
                    cache_entries.add(f"+CacheRecordPath={rel_dir}/*.{ext}")

                elif ext in self.music_extensions:
                    music_entries.add(f"+MusicPath={rel_dir}")

                elif ext in self.content_extensions:
                    path_entries.add(f"+Paths={rel_dir}/*.{ext}")

        all_lines = ["[Core.System]"]
        all_lines.extend(sorted(cache_entries | music_entries | path_entries))

        return "\r\n".join(all_lines) + "\r\n"
