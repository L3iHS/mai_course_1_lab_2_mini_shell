from pathlib import Path
from commands_registry import get_command, all_commands
from logger import get_logger


def parse(line: str):
    parts = [p for p in line.strip().split() if p]
    if not parts:
        return "", []
    return parts[0], parts[1:]


def main():
    logger = get_logger()
    cwd = Path.cwd()
    env = {"cwd": cwd, "undo": []}
    print("MiniShell (help: 'help', exit: 'exit')")

    while True:
        try:
            line = input(f"{cwd.name if cwd.name else "/"}> ") # если будет корневой каталог, то name будет пустым
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not line.strip():
            continue
        if line.strip() in ("exit", "quit"):
            break
        if line.strip() == "help":
            print("Команды:", ", ".join(all_commands()) or "(пока пусто)")
            continue

        logger.info(line)

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
    main()