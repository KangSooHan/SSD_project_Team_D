from shell.commands.base import Command
from ssd.abstract_ssd import AbstractSSD

class WriteCommand:
    def __init__(self, ssd: AbstractSSD):
        self._ssd = ssd

    def execute(self, lba, value) -> None:
        self._ssd.write(lba, value)