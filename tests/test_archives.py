from src.main import run_once


def test_zip_unzip(tmp_path):
    # подготовка каталога
    src = tmp_path / "srcdir"
    src.mkdir(parents=True, exist_ok=True)
    (src / "file.txt").write_text("data")

    # zip
    run_once(f"zip {src} arc.zip", cwd=tmp_path)
    assert (tmp_path / "arc.zip").exists()

    # unzip — текущая реализация распаковывает прямо в текущую директорию
    run_once("unzip arc.zip", cwd=tmp_path)

    # Проверяем, что файл появился в текущей папке
    assert (tmp_path / "file.txt").exists()


def test_tar_untar(tmp_path):
    src = tmp_path / "folder"
    src.mkdir(parents=True, exist_ok=True)
    (src / "f.txt").write_text("x")

    # tar
    run_once(f"tar {src} data.tar.gz", cwd=tmp_path)
    assert (tmp_path / "data.tar.gz").exists()

    # untar — создаёт папку folder/
    run_once("untar data.tar.gz", cwd=tmp_path)
    extracted = tmp_path / "folder"
    assert extracted.is_dir()
    assert (extracted / "f.txt").exists()