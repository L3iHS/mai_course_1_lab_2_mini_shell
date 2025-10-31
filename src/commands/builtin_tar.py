import tarfile

from pathlib import Path
from src.commands.base import Command
from src.paths import to_path


class Tar(Command):
    """
    Создание TAR.GZ архива
    """

    name = "tar"
    help = "tar <folder> <archive.tar.gz>"
    description = (
        "Создаёт архив TAR.GZ из указанного каталога\n\
        Пример:\n\
            tar src archive.tar.gz"
    )

    def run(self, args: list[str], cwd: Path, env: dict) -> None:
        if len(args) != 2:
            raise ValueError("Использование: tar <папка> <архив.tar.gz>")

        folder = to_path(args[0], cwd)
        archive = to_path(args[1], cwd)

        if not folder.exists() or not folder.is_dir():
            raise FileNotFoundError("Указанный путь не является каталогом")

        with tarfile.open(archive, "w:gz") as tarf:
            tarf.add(folder, arcname=folder.name)
        print(f"Архив {archive} успешно создан")