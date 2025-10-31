from src.main import run_once

def test_cp_and_mv(tmp_path):
    (tmp_path / "a.txt").write_text("A")
    run_once("cp a.txt b.txt", cwd=tmp_path)
    assert (tmp_path / "b.txt").exists()

    run_once("mv b.txt c.txt", cwd=tmp_path)
    assert not (tmp_path / "b.txt").exists()
    assert (tmp_path / "c.txt").exists()

def test_rm_and_undo(tmp_path):
    p = tmp_path / "del.txt"
    p.write_text("bye")

    cwd, env = run_once("rm del.txt", cwd=tmp_path)
    assert not p.exists()

    cwd, env = run_once("undo", cwd=tmp_path, env=env)
    assert p.exists()