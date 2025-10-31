from src.commands.builtin_ls import Ls
from src.commands.builtin_cd import Cd
from src.commands.builtin_cat import Cat
from src.commands.builtin_cp import Cp
from src.commands.builtin_mv import Mv
from src.commands.builtin_rm import Rm
from src.commands.builtin_history import HistoryCmd
from src.commands.builtin_undo import Undo


COMMANDS = {
    "ls": Ls(),
    "cd": Cd(),
    "cat": Cat(),
    "cp": Cp(),
    "mv": Mv(),
    "rm": Rm(),
    "history": HistoryCmd(),
    "undo": Undo()
}


def get_command(name):
    """Возвращает объект команды"""
    return COMMANDS.get(name)


def all_commands():
    """Отсортированный список команд для help"""
    return sorted(COMMANDS.keys())