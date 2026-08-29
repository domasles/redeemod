from frontend.logic import (
    ToggleOutcome,
    assemble_launch_paths,
    can_open_library,
    get_launch_button_text,
    toggle_mod,
)


def test_toggle_selects_without_limit():
    selected, outcome = toggle_mod(set(), "Mod", True, None, True)

    assert selected == {"Mod"}
    assert outcome is ToggleOutcome.SELECTED


def test_toggle_deselects():
    selected, outcome = toggle_mod({"Mod", "Other"}, "Mod", False, None, True)

    assert selected == {"Other"}
    assert outcome is ToggleOutcome.DESELECTED


def test_toggle_is_blocked_by_limit():
    selected, outcome = toggle_mod({"One"}, "Two", True, 1, True)

    assert selected == {"One"}
    assert outcome is ToggleOutcome.LIMIT_REACHED


def test_toggle_allows_removing_when_limit_reached():
    selected, outcome = toggle_mod({"One", "Two"}, "One", False, 1, True)

    assert selected == {"Two"}
    assert outcome is ToggleOutcome.DESELECTED


def test_toggle_treats_missing_mod_as_missing():
    selected, outcome = toggle_mod({"Mod"}, "Mod", True, None, False)

    assert "Mod" not in selected
    assert outcome is ToggleOutcome.MISSING


def test_toggle_unlimited_when_allowed_mod_amount_is_none():
    selected, outcome = toggle_mod({"A", "B", "C"}, "D", True, None, True)

    assert selected == {"A", "B", "C", "D"}
    assert outcome is ToggleOutcome.SELECTED


def test_assemble_launch_paths_ordered_and_filtered(tmp_path):
    existing = tmp_path / "exists"
    existing.mkdir()

    all_mods = {
        "B": str(existing),
        "A": str(tmp_path / "missing"),
    }

    paths = assemble_launch_paths(all_mods, {"B", "A", "C"})
    assert paths == [existing]


def test_assemble_launch_paths_empty_selection(tmp_path):
    assert assemble_launch_paths({}, set()) == []


def test_launch_button_text():
    assert get_launch_button_text(set()) == "Launch standalone"
    assert get_launch_button_text({"Mod"}) == "Launch with mods"


def test_can_open_library():
    assert can_open_library(["ut99"]) is True
    assert can_open_library([]) is False
