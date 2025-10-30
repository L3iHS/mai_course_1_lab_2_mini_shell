COMMANDS = {}


def get_command(name):
    """Возвращает объект команды по имени или None."""
    return COMMANDS.get(name)


def all_commands():
    """Отсортированный список доступных имен команд (для help)."""
    return sorted(COMMANDS.keys())