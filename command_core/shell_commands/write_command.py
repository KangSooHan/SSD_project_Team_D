from ssd_core.abstract_ssd import AbstractSSD
from command_core.base_command import BaseCommand

class WriteCommand(BaseCommand):
    def __init__(self, ssd: AbstractSSD, lba: int, value: str):
        self._ssd = ssd
        self._lba = lba
        self._value = value

    def execute(self) -> None:
        if self._lba < 0 or self._lba > 99:
            raise Exception
        self._ssd.write(self._lba, self._value)
        print('[Write] Done')