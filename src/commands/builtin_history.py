from pathlib import Path
from src.commands.base import Command


HISTORY_FILE = Path("src/data/.history")


class HistoryCmd(Command):
    """
    История введённых команд
    """

    name = "history"
    help = "history [N]"
    description = (
        "Показывает последние N введённых команд\n\
        История сохраняется между запусками\n\
        Пример: history 10"
    )

    def run(self, args: list[str], cwd: Path, env: dict) -> None:
        n = int(args[0]) if args else 20
        if not HISTORY_FILE.exists():
            print("(История пока пуста)")
            return

        lines = HISTORY_FILE.read_text(encoding="utf-8").splitlines()
        for i, cmd in enumerate(lines[-n:], start=max(1, len(lines) - n + 1)):
            print(f"{i}: {cmd}")