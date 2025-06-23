from shell_core.abstract_ssd_driver import AbstractSSDDriver
from command_core.base_command import BaseCommand

class ReadCommand(BaseCommand):
    def __init__(self, ssd: AbstractSSDDriver, lba: int):
        self._ssd = ssd
        self._lba = lba

    def execute(self) -> None:
        if self._lba < 0 or self._lba > 99:
            raise Exception
        result = self._ssd.read(self._lba)
        print(f"[Read] LBA {self._lba:02d} : {result}")
