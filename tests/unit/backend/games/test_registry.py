import pytest

from backend.games import ADAPTERS, get_adapter_class, get_adapter_classes


def test_all_games_registered():
    classes = get_adapter_classes()
    assert set(classes) == {"ut99", "unrgold", "ut2k4", "ioq3"}


def test_registry_reads_class_attributes_without_instantiation():
    classes = get_adapter_classes()

    assert classes["ut99"].game_id == "ut99"
    assert classes["ut99"].display_name == "Unreal Tournament '99"
    assert classes["ioq3"].display_name == "IOQuake 3"


def test_adapter_class_matches():
    classes = get_adapter_classes()

    for game_id, adapter_class in classes.items():
        assert adapter_class in ADAPTERS
        assert adapter_class.game_id == game_id


def test_get_adapter_class_unknown_raises():
    with pytest.raises(ValueError):
        get_adapter_class("nope")
