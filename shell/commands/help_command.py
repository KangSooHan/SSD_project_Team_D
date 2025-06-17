from shell.commands.base import Command
from ssd.abstract_ssd import AbstractSSD

class HelpCommand:
    def __init__(self, ssd: AbstractSSD):
        self._ssd = ssd

    def execute(self) -> None:
        self._ssd.write("")
        return True