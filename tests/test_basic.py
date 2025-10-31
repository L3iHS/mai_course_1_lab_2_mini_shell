from pathlib import Path
from src.main import run_once


def test_ls_and_cd(capsys, tmp_path):
    (tmp_path / "dirA").mkdir()
    (tmp_path / "file.txt").write_text("hello", encoding="utf-8")

    run_once("ls", cwd=tmp_path)
    out = capsys.readouterr().out
    assert "dirA" in out
    assert "file.txt" in out

    cwd, env = run_once("cd dirA", cwd=tmp_path)
    assert cwd == tmp_path / "dirA"

    cwd, env = run_once("cd ..", cwd=cwd, env=env)
    assert cwd == tmp_path


def test_cat_file_and_error_on_dir(capsys, tmp_path):
    (tmp_path / "note.txt").write_text("content", encoding="utf-8")

    run_once("cat note.txt", cwd=tmp_path)
    out = capsys.readouterr().out
    assert "content" in out

    run_once("cat .", cwd=tmp_path)
    out = capsys.readouterr().out
    assert "Ошибка:" in out