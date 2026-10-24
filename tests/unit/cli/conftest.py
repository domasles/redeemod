import pytest

from backend.manager import Manager


@pytest.fixture
def manager(tmp_path) -> Manager:
    return Manager(storage_file=tmp_path / "settings.json")
