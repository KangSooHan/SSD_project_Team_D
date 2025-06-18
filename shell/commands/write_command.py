from shell.commands.base import Command
from ssd.abstract_ssd import AbstractSSD
import re

class WriteCommand:
    def __init__(self, ssd: AbstractSSD):
        self._ssd = ssd

    def execute(self, lba:int, value:str) -> None:
        if lba < 0 or lba > 99 :
            raise Exception
        if not self._is_valid_hex_regex(value):
            raise Exception
        self._ssd.write(lba, value)

    def _is_valid_hex_regex(self, value: str) -> bool:
        return bool(re.fullmatch(r'0x[0-9A-Fa-f]{8}', value))