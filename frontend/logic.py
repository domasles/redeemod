from __future__ import annotations

from pathlib import Path
from enum import Enum


class ToggleOutcome(Enum):
    """Result of a mod selection toggle."""

    SELECTED = "selected"
    DESELECTED = "deselected"
    LIMIT_REACHED = "limit_reached"
    MISSING = "missing"


def toggle_mod(
    selected: set[str],
    mod_name: str,
    enabled: bool,
    allowed_mod_amount: int | None,
    mod_exists: bool,
) -> tuple[set[str], ToggleOutcome]:
    """Applies a toggle to the selection and returns the new selection with its outcome."""

    new_selected = set(selected)

    if enabled:
        if allowed_mod_amount is not None and len(new_selected) >= allowed_mod_amount:
            return new_selected, ToggleOutcome.LIMIT_REACHED

        new_selected.add(mod_name)
        outcome = ToggleOutcome.SELECTED

    else:
        new_selected.discard(mod_name)
        outcome = ToggleOutcome.DESELECTED

    if not mod_exists:
        new_selected.discard(mod_name)
        return new_selected, ToggleOutcome.MISSING

    return new_selected, outcome


def assemble_launch_paths(all_mods: dict[str, str], selected_mods: set[str]) -> list[Path]:
    """Builds the ordered list of on-disk mod paths passed to the launcher."""

    selected_paths: list[Path] = []

    for name in sorted(selected_mods):
        if name not in all_mods:
            continue

        path = Path(all_mods[name])

        if path.exists():
            selected_paths.append(path)

    return selected_paths


def get_launch_button_text(selected_mods: set[str]) -> str:
    """Returns the launch button label for the given selection."""

    if len(selected_mods) == 0:
        return "Launch standalone"

    return "Launch with mods"


def can_open_library(added_games: list[str]) -> bool:
    """Whether the library screen may be shown given the added games."""
    return bool(added_games)
