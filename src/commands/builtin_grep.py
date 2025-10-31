import re
from pathlib import Path
from src.commands.base import Command
from src.paths import to_path


class Grep(Command):
    """
    Поиск текста в файлах
    """

    name = "grep"
    help = "grep [-r] [-i] <pattern> <path>"
    description = (
        "Ищет строки, соответствующие шаблону в указанных файлах.\n\
        Поддерживает:\n\
            -r — рекурсивный поиск\n\
            -i — поиск без учёта регистра\n\
        Пример:\n\
            grep main src/\n"
    )

    def run(self, args: list[str], cwd: Path, env: dict) -> None:
        if len(args) < 2:
            raise ValueError("Использование: grep [-r] [-i] <pattern> <path>")

        recursive = "-r" in args
        ignore_case = "-i" in args
        args = [a for a in args if a not in ("-r", "-i")]

        pattern, path_str = args[0], args[1]
        path = to_path(path_str, cwd)

        if not path.exists():
            raise FileNotFoundError(f"{path} не найден")

        flags = re.IGNORECASE if ignore_case else 0
        regex = re.compile(pattern, flags)

        files = []
        if path.is_file():
            files = [path]
        elif path.is_dir():
            if recursive:
                files = [p for p in path.rglob("*") if p.is_file()]
            else:
                files = [p for p in path.iterdir() if p.is_file()]
        else:
            raise ValueError("Указан неверный путь")

        matches = 0
        for file in files:
            try:
                with open(file, "r", encoding="utf-8", errors="ignore") as f:
                    for lineno, line in enumerate(f, start=1):
                        if regex.search(line):
                            matches += 1
                            print(f"{file}:{lineno}:{line.strip()}")
            except Exception as e:
                print(f"Ошибка при чтении {file}: {e}")

        if matches == 0:
            print("Совпадений не найдено")