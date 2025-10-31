from pathlib import Path
from datetime import datetime
import stat

from commands.base import Command
from paths import to_path


def format_long(p: Path) -> str:
    """для флага -l: права, размер, дата, имя"""
    s = p.stat() # чтобы получить инфу о правах доступа
    perms = stat.filemode(s.st_mode)
    size = f"{s.st_size:>8}"
    dt = datetime.fromtimestamp(s.st_mtime).strftime("%Y-%m-%d %H:%M")
    return f"{perms} {size} {dt} {p.name}"


class Ls(Command):
    """
    Выводит содержимое каталога
    """

    name = "ls"
    help = "ls [-l] [path]"

    def run(self, args: list[str], cwd: Path, env: dict) -> Path | None:
        long = False
        target_arg = None

        for a in args:
            if a == "-l":
                long = True
            else:
                target_arg = a

        target = to_path(target_arg, cwd)

        if not target.exists():
            raise FileNotFoundError("Нет такого файла или каталога")

        if target.is_file():
            print(format_long(target) if long else target.name)
            return None

        entries = sorted(target.iterdir(), key=lambda p: p.name.lower())  # .iterdir - содержимое каталога
        for p in entries:
            print(format_long(p) if long else p.name)

        return None