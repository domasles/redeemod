import zipfile

from dataclasses import dataclass
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

TEAM_ARENA_CHECKSUMS = {
    3162589758,
    4042724322,
    609103545,
    356785886,
}


@dataclass
class ModProfile:
    is_missionpack: bool = False
    is_standalone: bool = False


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

    def build_arguments(self, executable: Path, selected_mod_paths: list[Path]) -> list[str]:
        cmd: list[str] = []

        self.quake_3_path = executable.parent / "baseq3"

        if selected_mod_paths:
            mod_path = selected_mod_paths[0]
            cmd = self._set_cvars(mod_path, self._analyze_mod(mod_path))

        else:
            if not self._verify_quake_3():
                raise FileNotFoundError(
                    "Launching standalone requires Quake 3 Arena to be installed.\n"
                    "Place valid Quake 3 Arena 'baseq3' assets alongside the IOQuake 3 executable."
                )

        return cmd

    def _set_cvars(self, mod_path: Path, profile: ModProfile) -> list[str]:
        cmd = ["+set", "fs_steampath", str(mod_path.parent)]

        if not profile.is_standalone and not self._verify_quake_3():
            raise ValueError(
                "This mod requires Quake 3 Arena to be installed.\n"
                "Place valid Quake 3 Arena 'baseq3' assets alongside the IOQuake 3 executable."
            )

        if profile.is_missionpack or not profile.is_standalone:
            cmd.extend(["+set", "fs_game", str(mod_path.name)])

        else:
            cmd.extend(["+set", "com_basegame", str(mod_path.name)])

        return cmd

    def _contains_quake_3(self, checksum: int) -> bool:
        return checksum in QUAKE_3_CHECKSUMS

    def _verify_quake_3(self) -> bool:
        """Checks if a valid Quake 3 Arena directory sits alongside the executable."""

        if not self.quake_3_path.is_dir():
            return False

        for item in self.scan_mod_directory(self.quake_3_path):
            if self._contains_quake_3(calculate_archive_adler32(item[0])):
                return True

        return False

    def _analyze_mod(self, mod_path: Path) -> ModProfile:
        """Scans a mod's .pk3 files and classifies the mod."""

        profile = ModProfile()

        for item, _ext in self.scan_mod_directory(mod_path):
            if item.parent != mod_path:
                raise FileNotFoundError("All .pk3 files must be under the selected mod's root.")

            asset_profile = self._classify_asset(item, mod_path)

            profile.is_missionpack |= asset_profile.is_missionpack
            profile.is_standalone |= asset_profile.is_standalone

        return profile

    def _classify_asset(self, item: Path, mod_path: Path) -> ModProfile:
        """Classifies a single .pk3 file and handles engine requirements."""

        checksum = calculate_archive_adler32(item)

        if self._contains_quake_3(checksum):
            raise ValueError(
                "It seems like this mod contains Quake 3 Arena files.\n"
                "Place valid Quake 3 Arena 'baseq3' assets alongside the IOQuake 3 executable.\n"
                "RedeeMOD can't launch original Quake 3 Arena as a mod."
            )

        profile = ModProfile()

        if checksum in TEAM_ARENA_CHECKSUMS:
            if mod_path.name != "missionpack":
                raise ValueError(
                    "It seems like this mod contains Team Arena files.\n"
                    "Rename the mod's folder to 'missionpack'."
                )  # fmt: skip

            profile.is_missionpack = True

        if zipfile.is_zipfile(item):
            with zipfile.ZipFile(item, "r") as z:
                profile.is_standalone = any(name.lower().endswith("default.cfg") for name in z.namelist())

        return profile
