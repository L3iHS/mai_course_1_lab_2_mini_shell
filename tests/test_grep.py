from src.main import run_once


def test_grep_simple(capsys, tmp_path):
    (tmp_path / "a.txt").write_text("Hello\nworld\nHELLO")

    # без -i — совпадений не будет
    run_once("grep hello a.txt", cwd=tmp_path)
    out = capsys.readouterr().out
    assert "Совпадений" in out or "нет" in out

    # с -i — найдёт обе строки
    run_once("grep -i hello a.txt", cwd=tmp_path)
    out = capsys.readouterr().out
    assert "HELLO" in out and "Hello" in out


def test_grep_recursive(capsys, tmp_path):
    search_dir = tmp_path / "search_dir"
    search_dir.mkdir()
    (search_dir / "one.txt").write_text("todo")
    (search_dir / "two.txt").write_text("TODO")

    run_once("grep -r -i todo search_dir", cwd=tmp_path)
    out = capsys.readouterr().out
    assert "one.txt" in out and "two.txt" in out