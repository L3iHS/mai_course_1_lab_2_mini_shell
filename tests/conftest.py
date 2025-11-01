import pytest
from src import main
from src.commands import builtin_history
from src.commands import builtin_rm


@pytest.fixture(autouse=True)
def sandbox(monkeypatch, tmp_path):
    """Работает во временной дирректории"""
    monkeypatch.chdir(tmp_path)
    history = tmp_path / "src" / "data" / ".history"
    trash = tmp_path / "src" / "data" / ".trash"
    trash.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(main, "HISTORY_FILE", history, raising=False)  # raising=False если нет атрибута пропустит
    monkeypatch.setattr(builtin_history, "HISTORY_FILE", history, raising=False)
    monkeypatch.setattr(builtin_rm, "TRASH_DIR", trash, raising=False)
    return tmp_path