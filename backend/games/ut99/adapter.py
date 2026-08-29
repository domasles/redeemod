from pathlib import Path

from backend.games.ut99.ini import prepend_to_ini_section
from backend.utils.filesystem import get_relative_path
from backend.games.base import BaseGameAdapter
from backend.constants import *


class UT99GameAdapter(BaseGameAdapter):
    game_id = "ut99"
    display_name = "Unreal Tournament '99"

    @property
    def logo(self) -> Path | None:
        return self.adapter_assets_path / "logo.svg"

    @property
    def file_extensions(self) -> set[str]:
        return self.all_extensions

    def __init__(self, custom_paths: dict[str, str] | None = None, **kwargs):
        super().__init__(custom_paths, **kwargs)

        self.content_extensions = {"u", "unr", "utx", "uax", "umx"}
        self.locale_extensions = {"int", "det", "frt", "est", "itt", "rut"}
        self.all_extensions = self.content_extensions | self.locale_extensions

    def build_arguments(self, executable: Path, selected_mod_paths: list[Path]) -> list[str]:
        cmd: list[str] = []
        config_path = self.resolved_path("config_path")

        if selected_mod_paths and config_path and config_path.exists():
            mod_ini_path = get_relative_path(
                executable.parent,
                self._apply_mods_to_ini(selected_mod_paths, executable.parent, config_path),
            )

            cmd.append(f"INI={mod_ini_path}")

        return cmd

    def _apply_mods_to_ini(self, mod_paths: list[Path], exe_base: Path, config_path: Path) -> Path:
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

        mod_ini_path = config_path.parent / f"{APP_NAME}.ini"
        mod_ini_path.parent.mkdir(parents=True, exist_ok=True)

        if new_content.strip():
            updated_ini = prepend_to_ini_section(config_path, "Core.System", new_content)
            mod_ini_path.write_text(updated_ini, "utf-8")

        return mod_ini_path
