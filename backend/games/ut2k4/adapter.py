import shutil

from pathlib import Path

from backend.utils.filesystem import get_relative_path
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
    def logo(self) -> Path | None:
        return self.adapter_assets_path / "logo.svg"

    @property
    def file_extensions(self) -> set[str]:
        return self.all_extensions

    def __init__(self, custom_paths: dict[str, str] | None = None):
        super().__init__(custom_paths)

        self.content_extensions = {"u", "ut2", "utx", "usx", "ukx", "uax", "upl"}
        self.music_extensions = {"ogg"}
        self.cache_extensions = {"ucl"}

        self.all_extensions = self.content_extensions | self.music_extensions | self.cache_extensions

    def build_arguments(self, executable: Path, selected_mod_paths: list[Path]) -> list[str]:
        cmd: list[str] = []
        config_path = self.resolved_path("config_path")

        if selected_mod_paths and config_path and config_path.exists():
            self._cleanup_generated_files()
            self._write_mod_files(selected_mod_paths, executable)

            cmd.append(f"-mod={APP_NAME}")

        return cmd

    def _cleanup_generated_files(self):
        cleaned_dirs = set()

        for cfg_path in self.resolved_paths("config_paths"):
            if not cfg_path:
                continue

            target_app_dir = cfg_path.parent.parent / APP_NAME

            if target_app_dir not in cleaned_dirs:
                cleaned_dirs.add(target_app_dir)

                if target_app_dir.exists():
                    shutil.rmtree(target_app_dir)

    def _write_mod_files(self, mod_paths: list[Path], executable: Path):
        exe_base = executable.parent

        install_dir = exe_base.parent
        app_mod_dir = install_dir / APP_NAME
        app_sys_dir = app_mod_dir / "System"

        app_sys_dir.mkdir(parents=True, exist_ok=True)

        ut2k4mod_content = (
            "[MOD]\r\n"
            'ModTitle="RedeeMOD"\r\n'
            'ModDesc="A package of selected mods through RedeeMOD launcher."\r\n'
        )  # fmt: skip

        default_ini_content = self._generate_default_ini(mod_paths, exe_base)

        (app_mod_dir / "UT2K4Mod.ini").write_text(ut2k4mod_content, "utf-8")
        (app_sys_dir / "Default.ini").write_text(default_ini_content, "utf-8")
        (app_sys_dir / "DefUser.ini").write_text("\r\n", "utf-8")

    def _generate_default_ini(self, mod_paths: list[Path], exe_base: Path) -> str:
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
