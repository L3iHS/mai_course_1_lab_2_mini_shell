import shutil

from pathlib import Path
from src.commands.base import Command


HISTORY_FILE = Path("src/data/.history")
TRASH_DIR = Path("src/data/.trash")
TRASH_DIR.mkdir(parents=True, exist_ok=True)


class Undo(Command):
    """
    Отмена последней операции cp, mv или rm
    """

    name = "undo"
    help = "undo"
    description = (
        "Отменяет последнюю команду из списка cp, mv или rm\n\
        Для cp: удаляет скопированный файл\n\
        Для mv: возвращает на исходное место\n\
        Для rm: восстанавливает из корзины (.trash)"
    )

    def run(self, args: list[str], cwd: Path, env: dict) -> None:
        if not HISTORY_FILE.exists():
            print("История пуста")
            return

        lines = HISTORY_FILE.read_text(encoding="utf-8").splitlines()
        if not lines:
            print("История пуста")
            return

        last = lines[-1]
        print(f"Отменяется: {last}")

        parts = last.split()
        if not parts:
            print("Невозможно отменить пустую команду")
            return

        cmd, *rest = parts
        try:
            if cmd == "cp" and len(rest) >= 2:
                dst = Path(rest[-1])
                if dst.exists():
                    if dst.is_dir():
                        shutil.rmtree(dst)
                    else:
                        dst.unlink()
                    print(f"Удалён {dst}")

            elif cmd == "mv" and len(rest) >= 2:
                src, dst = Path(rest[0]), Path(rest[-1])
                if dst.exists():
                    shutil.move(dst, src)
                    print(f"Файл возвращён: {dst} → {src}")

            elif cmd == "rm" and len(rest) >= 1:
                name = Path(rest[0]).name
                trash_item = TRASH_DIR / name
                if trash_item.exists():
                    shutil.move(trash_item, cwd / name)
                    print(f"Восстановлен: {name}")

            else:
                print("Эту команду нельзя отменить")

        except Exception as e:
            print(f"Ошибка при отмене: {e}")