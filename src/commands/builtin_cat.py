from pathlib import Path
from src.commands.base import Command
from src.paths import to_path


class Cat(Command):
    """
    Вывод содержимого файла в консоль
    """

    name = "cat"
    help = "cat <file>"
    description = (
        "Показывает содержимое указанного файла\n\
        Если указан каталог или путь не существует,то выводит ошибку"
    )

    def run(self, args: list[str], cwd: Path, env: dict) -> None:
        if not args:
            raise ValueError("Нужно указать имя файла")

        target = to_path(args[0], cwd)

        if not target.exists():
            raise FileNotFoundError("Файл не найден")
        if target.is_dir():
            raise IsADirectoryError("Указан каталог, а не файл")

        try:
            text = target.read_text(encoding="utf-8")  # read_text из pathlib
            print(text)
        except PermissionError:
            raise PermissionError("Недостаточно прав для чтения файла")