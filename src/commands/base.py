from pathlib import Path


class Command:
    """
    Базовый класс для всех команд
    чтобы удобнее пользоваться getattr
    """

    name: str               # имя команды
    help: str               # инфа о команде (типо как использовать, синтаксис)
    description: str = ""   # подробное описание

    def run(self, args: list[str], cwd: Path, env: dict) -> Path | None:
        """
        Выполняет команду
        
        - args: список аргументов
        - cwd: текущий рабочий каталог
        - env: для undo 
        """
        raise NotImplementedError("Метод run() должен быть переопределён")