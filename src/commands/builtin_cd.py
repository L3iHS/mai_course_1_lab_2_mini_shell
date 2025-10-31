from pathlib import Path
from src.commands.base import Command
from src.paths import to_path


class Cd(Command):
    """
    Смена текущего каталога
    """

    name = "cd"
    help = "cd <path>"

    def run(self, args: list[str], cwd: Path, env: dict) -> Path | None:
        if not args:
            raise ValueError("Нужно указать путь")

        target = to_path(args[0], cwd)  # меняем cwd на переданный путь

        if not target.exists():
            raise FileNotFoundError("Каталог не существует")
        if not target.is_dir():
            raise NotADirectoryError("Это не каталог")

        return target