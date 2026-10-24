from pathlib import Path

from backend.manager import Manager


def remove_mods(manager: Manager, game_id: str, mod_refs: list[str]) -> None:
    mods = manager.get_mods(game_id)

    for ref in mod_refs:
        mod_name = ref

        if ref not in mods:
            matches = [name for name, path in mods.items() if str(Path(path)) == str(Path(ref))]

            if not matches:
                raise ValueError(f"Mod not found: {ref}")

            mod_name = matches[0]

        manager.remove_mod(game_id, mod_name)
