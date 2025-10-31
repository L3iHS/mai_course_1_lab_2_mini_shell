import pytest
from pathlib import Path
from src import main as main_mod
from src.commands import builtin_history as hist_mod
from src.commands import builtin_rm as rm_mod

@pytest.fixture(autouse=True)
def sandbox(monkeypatch, tmp_path):
    """Работает во временной дирректории"""
    monkeypatch.chdir(tmp_path)
    history = tmp_path / "src" / "data" / ".history"
    trash = tmp_path / "src" / "data" / ".trash"
    trash.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(main_mod, "HISTORY_FILE", history, raising=False)
    monkeypatch.setattr(hist_mod, "HISTORY_FILE", history, raising=False)
    monkeypatch.setattr(rm_mod, "TRASH_DIR", trash, raising=False)
    return tmp_path