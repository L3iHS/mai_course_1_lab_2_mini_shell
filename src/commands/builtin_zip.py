import zipfile

from pathlib import Path
from src.commands.base import Command
from src.paths import to_path


class Zip(Command):
    """
    Создание ZIP-архива из каталога
    """

    name = "zip"
    help = "zip <folder> <archive.zip>"
    description = (
        "Создаёт ZIP-архив из указанной папки\n\
        Пример:\n\
            zip src archive.zip"
    )

    def run(self, args: list[str], cwd: Path, env: dict) -> None:
        if len(args) != 2:
            raise ValueError("Использование: zip <папка> <архив.zip>")

        folder = to_path(args[0], cwd)
        archive = to_path(args[1], cwd)

        if not folder.exists() or not folder.is_dir():
            raise FileNotFoundError(f"{folder} не существует или не является каталогом")

        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file in folder.rglob("*"):
                zipf.write(file, file.relative_to(folder)) # путь внутри архива относительно папки
        print(f"Архив {archive} успешно создан")