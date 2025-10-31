from pathlib import Path


HOME = Path.home()


def to_path(arg, cwd: Path) -> Path:
    """
    Преобразует ввод пользователя в абсолютный Path
    """
    if arg is None or str(arg).strip() == "":
        return cwd

    s = str(arg).strip().strip('"').strip("'")

    if s == "~":
        p = HOME
    elif s.startswith("~/"):
        p = HOME / s[2:]
    else:
        p = Path(s)
        if not p.is_absolute():
            p = cwd / p

    return p.resolve(strict=False)


def forbid_dangerous_delete(p: Path) -> None:
    """
    Вызывает PermissionError, если попытались удалить кореневой каталог или ..
    """
    rp = p.resolve(strict=False)

    root = Path(rp.anchor) # возвращает корневой каталог в зависомисти от системы
    if rp == root:
        raise PermissionError("Удаление корневого каталога запрещено")

    if rp.name == "..":
        raise PermissionError("Удаление '..' запрещено")