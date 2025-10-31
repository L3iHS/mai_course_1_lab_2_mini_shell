from src.main import run_once

def test_ls_and_cd(capsys, tmp_path):
    (tmp_path / "dirA").mkdir()
    (tmp_path / "file.txt").write_text("hello")
    run_once("ls", cwd=tmp_path)
    out = capsys.readouterr().out
    assert "dirA" in out and "file.txt" in out

    cwd, env = run_once("cd dirA", cwd=tmp_path)
    assert cwd == tmp_path / "dirA"

    cwd, env = run_once("cd ..", cwd=cwd, env=env)
    assert cwd == tmp_path

def test_cat_file_and_error(capsys, tmp_path):
    f = tmp_path / "note.txt"
    f.write_text("hi")
    run_once("cat note.txt", cwd=tmp_path)
    out = capsys.readouterr().out
    assert "hi" in out

    run_once("cat .", cwd=tmp_path)
    out = capsys.readouterr().out
    assert "Ошибка:" in out