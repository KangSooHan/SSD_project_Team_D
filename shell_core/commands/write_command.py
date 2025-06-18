from shell_core.commands.base import Command
from ssd_core.abstract_ssd import AbstractSSD
import re

class WriteCommand:
    def __init__(self, ssd: AbstractSSD):
        self._ssd = ssd

    def execute(self, lba:int, value:int) -> None:
        self._ssd.write(lba, value)
