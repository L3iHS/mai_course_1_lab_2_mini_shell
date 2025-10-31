from pathlib import Path
from src.commands_registry import get_command, all_commands
from src.logger import get_logger
import typer


app = typer.Typer(help="Мини-оболочка с файловыми командами")


@app.command(help="Показать содержимое каталога")
def ls(args: list[str] = typer.Argument(None, help="Аргументы ls")) -> None:
    """
    Список файлов и каталогов

    Поддерживает:
        - 'ls' — выводит список файлов в текущей директории
        - 'ls path' — показывает содержимое указанного пути
        - 'ls -l' — подробный формат (права, размер, дата, имя)

    Примеры:
        python -m src.main ls
        python -m src.main ls -l src
    """
    run_once("ls " + " ".join(args or []))


@app.command(help="Сменить каталог")
def cd(args: list[str] = typer.Argument(None, help="Путь")) -> None:
    """
    Меняет текущий рабочий каталог.

    Поддерживает:
        - 'cd <путь>' — переход в указанный каталог
        - 'cd ..' — переход на уровень выше
        - 'cd ~' — переход в домашнюю директорию

    Примеры:
        python -m src.main cd ..
        python -m src.main cd ~/Documents
    """
    run_once("cd " + " ".join(args or []))

@app.command(help="Показать содержимое файла")
def cat(args: list[str] = typer.Argument(None, help="Путь к файлу")) -> None:
    """
    Выводит содержимое файла в консоль

    Поддерживает:
        - 'cat <файл>' — показать содержимое файла
        - если указан каталог или путь не существует — выводит ошибку

    Примеры:
        python -m src.main cat README.md
        python -m src.main cat src/main.py
    """
    run_once("cat " + " ".join(args or []))


@app.command(name="exec", help='Выполнить одну команду')
def exec_once(cmd: str) -> None:
    """
    Выполняет одну произвольную команду оболочки
    Пример:
        python -m src.main exec "ls -l"
    """
    run_once(cmd)


def parse(line: str):
    """Разбивает строку на аргументы, учитывая кавычки и пробелы"""
    args = []
    current = ""
    quote = None

    for ch in line:
        if quote:  # зашли в кавычки
            if ch == quote:
                quote = None  # конец кавычек
            else:
                current += ch
        else:
            if ch in ("'", '"'):
                quote = ch
            elif ch.isspace():
                if current:
                    args.append(current)
                    current = ""
            else:
                current += ch

    if quote is not None:
        raise ValueError("Не все кавычки закрыты")
    
    if current:
        args.append(current)

    if not args:
        return "", []
    return args[0], args[1:]


def print_help_overview() -> None:
    """Печатает список всех команд с их кратким описанием"""
    names = all_commands()
    if not names:
        print("(команды пока не зарегистрированы)")
        return
    maxw = max(len(n) for n in names)
    print("Доступные команды:")
    for name in names:
        cmd = get_command(name)
        synopsis = getattr(cmd, "help", "").strip()  # возвращает атрибут конкретной команды, еслои его нет, то ничего
        print(f"  {name.ljust(maxw)}  {synopsis}")


def print_help_for(name: str) -> None:
    """Печатает подробную справку команде"""
    cmd = get_command(name)
    if not cmd:
        print(f"Неизвестная команда: {name}")
        return
    usage = getattr(cmd, "help", "").strip() or name
    desc = getattr(cmd, "description", "").strip()
    print(f"Использование: {usage}")
    if desc:
        print("\nОписание:")
        print(desc)


def run_once(cmd: str, cwd: Path | None = None, env: dict | None = None) -> tuple[Path, dict]:
    """
    Выполняет одну команду
    """

    logger = get_logger()
    cwd = cwd or Path.cwd()
    env = env or {"cwd": cwd, "undo": []}

    logger.info(cmd)

    name, args = parse(cmd)
    command = get_command(name)
    if not command:
        print(f"Неизвестная команда: {name}")
        logger.info("ERROR: Unknown command")
        return cwd, env

    try:
        new_cwd = command.run(args, cwd, env)
        if new_cwd is not None:
            cwd = new_cwd
    except Exception as exc:
        print(f"Ошибка: {exc}")
        logger.info(f"ERROR: {exc}")

    return cwd, env


@app.command(help="Запустить интерактивную оболочку")
def run_repl():
    """
    Запускает интерактивную мини-оболочку
    Команды:
        help — список доступных команд
        exit — выход
    """

    logger = get_logger()
    cwd = Path.cwd()
    env = {"cwd": cwd, "undo": []}
    print("MiniShell (help: 'help', exit: 'exit')")

    while True:
        try:
            prompt = cwd.name if cwd.name else "/"
            line = input(f"{prompt}> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not line.strip():
            continue

        logger.info(line)

        if line.strip() in ("exit", "quit"):
            break
        if line.strip() == "help":
            print_help_overview()  # выводит все команды с синтаксисом использования
            continue
        if line.strip().endswith("--help"):
            name, _ = parse(line)
            print_help_for(name)
            continue

        name, args = parse(line)
        cmd = get_command(name)
        if not cmd:
            print(f"Неизвестная команда: {name}")
            logger.info("ERROR: Unknown command")
            continue

        try:
            new_cwd = cmd.run(args, cwd, env)
            if new_cwd is not None:
                cwd = new_cwd
        except Exception as e:
            print("Ошибка:", e)
            logger.info(f"ERROR: {e}")

if __name__ == "__main__":
    # python -m src.main run-repl
    # python -m src.main run-repl --help
    app()