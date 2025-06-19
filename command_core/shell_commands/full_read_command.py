from ssd_core.abstract_ssd import AbstractSSD
from command_core.base_command import BaseCommand

class FullReadCommand(BaseCommand):
    def __init__(self, ssd: AbstractSSD):
        self._ssd = ssd
        self._loop_count = 100

    def execute(self) -> None:
        for lba in range(self._loop_count) :
            result = self._ssd.read(lba)
            print(f"[Read] LBA {lba:02d} : {result}")
