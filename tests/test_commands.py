import pytest
from pathlib import Path

from src.commands.builtin_cd import Cd
from src.commands.builtin_cat import Cat
from src.commands.builtin_cp import Cp
from src.commands.builtin_mv import Mv
from src.commands.builtin_rm import Rm, TRASH_DIR
from src.commands.builtin_grep import Grep
from src.commands.builtin_zip import Zip
from src.commands.builtin_unzip import Unzip
from src.commands.builtin_tar import Tar
from src.commands.builtin_untar import Untar


class TestCd:
    def setup_method(self):
        self.cd = Cd()

    def test_cd_changes_directory(self, tmp_path):
        target = tmp_path / "dirA"
        target.mkdir()
        new_cwd = self.cd.run(["dirA"], cwd=tmp_path, env={})
        assert new_cwd == target

    def test_cd_errors(self, tmp_path):
        # проверяем что произошло ожидаемая ошибка 
        with pytest.raises(ValueError):
            self.cd.run([], cwd=tmp_path, env={})

        with pytest.raises(FileNotFoundError):
            self.cd.run(["no_dir"], cwd=tmp_path, env={})

        file_path = tmp_path / "file.txt"
        file_path.write_text("data")
        with pytest.raises(NotADirectoryError):
            self.cd.run(["file.txt"], cwd=tmp_path, env={})


class TestCat:
    def setup_method(self):
        self.cat = Cat()

    def test_cat_prints_file_content(self, tmp_path, capsys):
        f = tmp_path / "note.txt"
        f.write_text("hello\nworld")

        self.cat.run(["note.txt"], cwd=tmp_path, env={})
        out = capsys.readouterr().out
        assert "hello" in out
        assert "world" in out

    def test_cat_errors(self, tmp_path):
        with pytest.raises(ValueError):
            self.cat.run([], cwd=tmp_path, env={})

        with pytest.raises(FileNotFoundError):
            self.cat.run(["error.txt"], cwd=tmp_path, env={})

        d = tmp_path / "dir"
        d.mkdir()
        with pytest.raises(IsADirectoryError):
            self.cat.run(["dir"], cwd=tmp_path, env={})


class TestCp:
    def setup_method(self):
        self.cp = Cp()

    def test_cp_copies_file(self, tmp_path):
        src = tmp_path / "a.txt"
        src.write_text("A")

        self.cp.run(["a.txt", "b.txt"], cwd=tmp_path, env={})

        dst = tmp_path / "b.txt"
        assert dst.exists()
        assert dst.read_text() == "A"

    def test_cp_dir_requires_recursive_flag(self, tmp_path):
        folder = tmp_path / "srcdir"
        folder.mkdir()
        (folder / "file.txt").write_text("x")

        with pytest.raises(IsADirectoryError):
            self.cp.run(["srcdir", "dst"], cwd=tmp_path, env={})

        self.cp.run(["-r", "srcdir", "dst"], cwd=tmp_path, env={})
        dst_folder = tmp_path / "dst"
        assert (dst_folder / "file.txt").exists()


class TestMv:
    def setup_method(self):
        self.mv = Mv()

    def test_mv_renames_file(self, tmp_path):
        src = tmp_path / "a.txt"
        src.write_text("A")

        self.mv.run(["a.txt", "b.txt"], cwd=tmp_path, env={})

        assert not src.exists()
        assert (tmp_path / "b.txt").exists()

    def test_mv_missing_source_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            self.mv.run(["none.txt", "dst.txt"], cwd=tmp_path, env={})


class TestRm:
    def setup_method(self):
        self.rm = Rm()

    def test_rm_moves_file_to_trash(self, tmp_path):
        f = tmp_path / "del.txt"
        f.write_text("bye")

        self.rm.run(["del.txt"], cwd=tmp_path, env={})

        assert not f.exists()
        trash_file = TRASH_DIR / "del.txt"
        assert trash_file.exists()

    def test_rm_dir_requires_r_flag(self, tmp_path, capsys):
        folder = tmp_path / "dir_to_remove"
        folder.mkdir()

        self.rm.run(["dir_to_remove"], cwd=tmp_path, env={})

        out = capsys.readouterr().out
        assert "Указан каталог, чтобы его рекурсивно удалить используйте флаг -r" in out
        assert folder.exists()

    def test_rm_dir_with_r_and_cancel(self, tmp_path, monkeypatch, capsys):
        folder = tmp_path / "dir_to_remove"
        folder.mkdir()
        
        # откланяем удаление чреез "n"
        monkeypatch.setattr("builtins.input", lambda _: "n")
        self.rm.run(["-r", "dir_to_remove"], cwd=tmp_path, env={})

        assert folder.exists()
        out = capsys.readouterr().out
        assert "Удаление отменено" in out


class TestGrep:
    def setup_method(self):
        self.grep = Grep()

    def test_grep_case_insensitive(self, tmp_path, capsys):
        f = tmp_path / "a.txt"
        f.write_text("Hello\nworld\nHELLO\n")

        self.grep.run(["hello", "a.txt"], cwd=tmp_path, env={})
        out1 = capsys.readouterr().out

        self.grep.run(["-i", "hello", "a.txt"], cwd=tmp_path, env={})
        out2 = capsys.readouterr().out

        assert "Совпадений" in out1 or "нет" in out1
        assert "Hello" in out2 and "HELLO" in out2

    def test_grep_no_matches_prints_message(self, tmp_path, capsys):
        f = tmp_path / "b.txt"
        f.write_text("aaa\nbbb\nccc\n")

        self.grep.run(["xxx", "b.txt"], cwd=tmp_path, env={})
        out = capsys.readouterr().out
        assert "Совпадений" in out or "не найдено" in out


class TestZipUnzip:
    def setup_method(self):
        self.zip_cmd = Zip()
        self.unzip_cmd = Unzip()

    def test_zip_and_unzip_roundtrip(self, tmp_path):
        srcdir = tmp_path / "srcdir"
        srcdir.mkdir()
        (srcdir / "file.txt").write_text("data")

        self.zip_cmd.run(["srcdir", "arc.zip"], cwd=tmp_path, env={})
        arc = tmp_path / "arc.zip"
        assert arc.exists()

        self.unzip_cmd.run(["arc.zip"], cwd=tmp_path, env={})

        extracted_file = tmp_path / "file.txt"
        assert extracted_file.exists()
        assert extracted_file.read_text() == "data"


class TestTarUntar:
    def setup_method(self):
        self.tar_cmd = Tar()
        self.untar_cmd = Untar()

    def test_tar_and_untar_roundtrip(self, tmp_path):
        folder = tmp_path / "folder"
        folder.mkdir()
        (folder / "f.txt").write_text("x")

        self.tar_cmd.run(["folder", "data.tar.gz"], cwd=tmp_path, env={})
        arc = tmp_path / "data.tar.gz"
        assert arc.exists()

        self.untar_cmd.run(["data.tar.gz"], cwd=tmp_path, env={})

        extracted = tmp_path / "folder"
        assert extracted.is_dir()
        assert (extracted / "f.txt").exists()