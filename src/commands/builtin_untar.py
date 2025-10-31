import tarfile
from pathlib import Path
from src.commands.base import Command
from src.paths import to_path


class Untar(Command):
    """
    Распаковка TAR.GZ архива
    """

    name = "untar"
    help = "untar <archive.tar.gz>"
    description = (
        "Распаковывает архив TAR.GZ в текущий каталог\n\
        Пример:\n\
            untar archive.tar.gz"
    )

    def run(self, args: list[str], cwd: Path, env: dict) -> None:
        if len(args) != 1:
            raise ValueError("Использование: untar <архив.tar.gz>")

        archive = to_path(args[0], cwd)
        if not archive.exists():
            raise FileNotFoundError("Архив не найден")

        with tarfile.open(archive, "r:gz") as tarf:
            tarf.extractall(cwd)
        print(f"Архив {archive.name} успешно распакован в {cwd}")