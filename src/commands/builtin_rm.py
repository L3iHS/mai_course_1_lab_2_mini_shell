import shutil
from pathlib import Path
from src.commands.base import Command
from src.paths import to_path


TRASH_DIR = Path("src/data/.trash")
TRASH_DIR.mkdir(parents=True, exist_ok=True)


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
            trash_target = TRASH_DIR / target.name

            if target.is_dir():
                if not recursive:
                    raise IsADirectoryError(
                        "Указан каталог, чтобы его рекурсивно удалить используйте флаг -r"
                    )

                confirm = input(f"Вы уверены, что хотите удалить {target}? (y/n): ")
                if confirm.lower() != "y":
                    print("Удаление отменено")
                    return

            # перемещаем в .trash вместо удаления
            shutil.move(str(target), str(trash_target))
            print(f"{target} перемещён в корзину (.trash)")

        except PermissionError:
            raise PermissionError("Недостаточно прав для удаления")
        except Exception as e:
            print(f"Ошибка при удалении: {e}")