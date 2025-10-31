import shutil

from pathlib import Path

from src.commands.base import Command
from src.paths import to_path


class Mv(Command):
    """
    Перемещение или переименование файлов и каталогов
    """

    name = "mv"
    help = "mv <source> <destination>"
    description = (
        "Перемещает или переименовывает файл или каталог\n\
        Если destination каталог,то объект будет перемещён внутрь него\n\
        Если destination имя файла, то объект переименуется\n\
        Примеры:\n\
            mv oldd.txt new.txt\n\
            mv dir_1/ dir_2/\n"
    )

    def run(self, args: list[str], cwd: Path, env: dict) -> None:
        if len(args) != 2:
            hint = ""
            if any(" " in a for a in args):
                hint = (
                    '\nПодсказка: если в пути есть пробелы, используйте для этого пути ковычки'
                )
            raise ValueError(
                f"Ожидается 2 аргумента: mv <source> <destination>"
                f"Получено: {len(args)}.{hint}"
            )

        src = to_path(args[0], cwd)
        dst = to_path(args[1], cwd)

        if not src.exists():
            raise FileNotFoundError("Источник не существует")

        try:
            shutil.move(src, dst)
        except PermissionError:
            raise PermissionError("Недостаточно прав для перемещения")
        except FileNotFoundError:
            raise FileNotFoundError("Путь назначения не существует")