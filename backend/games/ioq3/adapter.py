import subprocess

from pathlib import Path

from backend.games.ioq3.checksum import calculate_archive_adler32
from backend.games.base import BaseGameAdapter

QUAKE_3_CHECKSUMS = {
    3006842482,
    3197754754,
    3232371534,
    1331829193,
    2238193561,
    1513501394,
    3770946489,
    2583176489,
    1594644322,
}


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
    def allowed_mod_amount(self) -> int:
        return 1

    @property
    def file_extensions(self) -> set[str]:
        return self.content_extensions

    def __init__(self, custom_paths: dict[str, str] | None = None):
        super().__init__(custom_paths)
        self.content_extensions = {"pk3"}

    def _validate_mod_asset(self, item: Path, mod_path: Path, ext: str) -> None:
        """Ensures correct directory for official Quake 3 Arena files."""

        if mod_path.name == "baseq3" or ext.lower() not in self.content_extensions:
            return

        checksum = calculate_archive_adler32(item)

        if checksum in QUAKE_3_CHECKSUMS:
            raise ValueError(
                "It seems like this mod contains Quake 3 Arena files.\n"
                "Please rename the mod's folder to 'baseq3'.\n\n"
                "This only applies to original Quake 3 Arena files."
            )

    def launch(self, selected_mod_paths: list[Path]) -> None:
        if not self.executable_path or not self.executable_path.exists():
            raise FileNotFoundError(f"{self.display_name} installation not found.")

        cmd = [str(self.executable_path)]

        if selected_mod_paths:
            mod_path = selected_mod_paths[0]

            for item, ext in self.scan_mod_directory(mod_path):
                if item.parent != mod_path:
                    raise FileNotFoundError("All .pk3 files must be under the selected mod's root.")

                self._validate_mod_asset(item, mod_path, ext)

            cmd.extend([
                "+set", "fs_steampath", str(mod_path.parent),
                "+set", "com_basegame", mod_path.name,
            ])  # fmt: skip

        subprocess.Popen(cmd, cwd=str(self.executable_path.parent))
