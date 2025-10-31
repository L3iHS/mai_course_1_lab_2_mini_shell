import shutil
from pathlib import Path
from src.commands.base import Command
from src.paths import to_path


class Cp(Command):
    """
    Копирование файлов и каталогов
    """

    name = "cp"
    help = "cp [-r] <source> <destination>"
    description = (
        "Копирует файл или каталог в указанное место\n\
        Поддерживает:\n\
            -r — рекурсивное копирование каталогов\n"
    )

    def run(self, args: list[str], cwd: Path, env: dict) -> None:
        recursive = False
        if "-r" in args:
            recursive = True
            args = [a for a in args if a != "-r"]

        if len(args) != 2:
            hint = ""
            if any(" " in a for a in args):
                hint = (
                    '\nПодсказка: если в пути есть пробелы, используйте для этого пути ковычки'
                )
            raise ValueError(
                f"Ожидается 2 аргумента: cp [-r] <source> <destination> "
                f"Получено: {len(args)}.{hint}"
            )

        src = to_path(args[0], cwd)
        dst = to_path(args[1], cwd)

        if not src.exists():
            raise FileNotFoundError("Источник не существует")

        try:
            if src.is_dir():
                if not recursive:
                    raise IsADirectoryError(
                        "Для копирования каталогов используйте -r"
                    )
                shutil.copytree(src, dst, dirs_exist_ok=True)  # dirs_exist_ok=True, чтобы перезаписывать
                # если dst не существует, то он создается
            else:
                shutil.copy2(src, dst)  # если dst файл, то он перезапишется
        except FileNotFoundError:
            raise FileNotFoundError("Второй путь не существует")
        except PermissionError:
            raise PermissionError("Недостаточно прав для копирования")