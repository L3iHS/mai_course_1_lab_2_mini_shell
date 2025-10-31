import pytest

@pytest.fixture(autouse=True)
def temp_dir(monkeypatch, tmp_path):
    """Просто выполняем каждый тест в отдельной временной директории."""
    monkeypatch.chdir(tmp_path)
    return tmp_path
