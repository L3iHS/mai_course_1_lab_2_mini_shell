from src.commands.builtin_ls import Ls
from src.commands.builtin_cd import Cd
from src.commands.builtin_cat import Cat
from src.commands.builtin_cp import Cp
from src.commands.builtin_mv import Mv
from src.commands.builtin_rm import Rm
from src.commands.builtin_history import HistoryCmd
from src.commands.builtin_undo import Undo
from src.commands.builtin_zip import Zip
from src.commands.builtin_unzip import Unzip
from src.commands.builtin_tar import Tar
from src.commands.builtin_untar import Untar
from src.commands.builtin_grep import Grep


COMMANDS = {
    "ls": Ls(),
    "cd": Cd(),
    "cat": Cat(),
    "cp": Cp(),
    "mv": Mv(),
    "rm": Rm(),
    "history": HistoryCmd(),
    "undo": Undo(),
    "zip": Zip(),
    "unzip": Unzip(),
    "tar": Tar(),
    "untar": Untar(),
    "grep": Grep()
}


def get_command(name):
    """Возвращает объект команды"""
    return COMMANDS.get(name)


def all_commands():
    """Отсортированный список команд для help"""
    return sorted(COMMANDS.keys())