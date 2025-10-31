import zipfile

from pathlib import Path
from src.commands.base import Command
from src.paths import to_path


class Unzip(Command):
    """
    Распаковка ZIP-архива
    """

    name = "unzip"
    help = "unzip <archive.zip>"
    description = (
        "Распаковывает архив ZIP в текущий каталог\n\
        Пример:\n\
            unzip backup.zip"
    )

    def run(self, args: list[str], cwd: Path, env: dict) -> None:
        if len(args) != 1:
            raise ValueError("Использование: unzip <archive.zip>")

        archive = to_path(args[0], cwd)
        if not archive.exists():
            raise FileNotFoundError("Архив не найден")

        with zipfile.ZipFile(archive, "r") as zipf:
            zipf.extractall(cwd)

        print(f"Архив {archive.name} успешно распакован в {cwd}")