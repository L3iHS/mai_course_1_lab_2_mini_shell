import shutil
from pathlib import Path
from src.commands.base import Command
from src.paths import to_path


class Rm(Command):
    """
    Удаление файлов и каталогов
    """

    name = "rm"
    help = "rm [-r] <path>"
    description = (
        "Удаляет указанный файл или каталог\n\
        Поддерживает:\n\
            -r — рекурсивное удаление каталогов с их содержимым\n\
        Требует подтверждения при удалении каталогов\n\
        Ограничения:\n\
            - нельзя удалить корень '/'\n\
            - нельзя удалить родительский каталог '..'\n\
        Примеры:\n\
            rm file.txt\n\
            rm -r old_folder/\n"
    )

    def run(self, args: list[str], cwd: Path, env: dict) -> None:
        if not args:
            raise ValueError("Нужно указать путь для удаления")

        recursive = False
        if "-r" in args:
            recursive = True
            args = [a for a in args if a != "-r"]

        if len(args) != 1:
            raise ValueError("Ожидается один путь")

        target = to_path(args[0], cwd)

        # Как указано в условиях 
        if target.name in ("/", ".."):
            raise PermissionError("Удаление этого каталога запрещено")

        if not target.exists():
            raise FileNotFoundError("Файл или каталог не существует")

        try:
            if target.is_dir():
                if not recursive:
                    raise IsADirectoryError(
                        "Указан каталог, чтобы его рекурсивно удалсить используйте флаг -r"
                    )

                confirm = input(f"Вы уверены, что хотите удалить {target}? (y/n): ")
                if confirm.lower() != "y":
                    print("Удаление отменено")
                    return

                shutil.rmtree(target)  # удаляет весь каталог рекурсивно
            else:
                target.unlink()  # удаляет файл

            print(f"{target} успешно удалён")
        except PermissionError:
            raise PermissionError("Недостаточно прав для удаления")