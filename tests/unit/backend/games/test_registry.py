import pytest

from backend.games import ADAPTERS, get_adapter_class, get_adapter_classes


def test_all_games_registered():
    classes = get_adapter_classes()
    assert set(classes) == {"ut99", "unrgold", "ut2k4", "ioq3"}


def test_adapter_class_matches():
    classes = get_adapter_classes()

    for game_id, adapter_class in classes.items():
        assert adapter_class in ADAPTERS
        assert adapter_class.game_id == game_id


def test_get_adapter_class_unknown_raises():
    with pytest.raises(ValueError):
        get_adapter_class("nope")
