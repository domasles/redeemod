from pathlib import Path

from backend.utils.filesystem import expand_path, get_base_directory, get_relative_path, get_project_directory
from backend.discovery import discover_installation, load_config
from backend.utils.ini import append_to_ini_file


exe, cfg = discover_installation(load_config(get_project_directory() / "backend/config/config.json"))
exe_base = get_base_directory(exe)

content_extensions = {"u", "unr", "utx", "uax", "umx"}
localization_extensions = {"int", "det", "frt", "est", "itt", "rut"}

directories = [
    Path("~/.local/share/OldUnreal/UnrealTournament/NW3Final"),
    Path("~/.local/share/OldUnreal/UnrealTournament/XVehiclesV74")
]

path_entries: set[str] = set()
lang_entries: set[str] = set()

for target_dir in directories:
    target_dir = expand_path(target_dir)

    if not target_dir.exists():
        continue

    for item in target_dir.rglob("*"):
        if not item.is_file():
            continue

        ext = item.suffix.lstrip(".").lower()
        rel_dir = get_relative_path(exe_base, item.parent)

        if ext in content_extensions:
            path_entries.add(f"Paths={rel_dir}/*.{ext}")

        elif ext in localization_extensions:
            lang_entries.add(f"LangPaths={rel_dir}/*.<lang>")

new_content = "\n".join(sorted(path_entries | lang_entries)) + "\n"

if new_content.strip():
    print(append_to_ini_file(cfg, "Core.System", new_content))
