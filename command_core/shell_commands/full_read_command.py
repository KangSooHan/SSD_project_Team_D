from shell_core.abstract_ssd_driver import AbstractSSDDriver
from command_core.base_command import BaseCommand

class FullReadCommand(BaseCommand):
    def __init__(self, ssd: AbstractSSDDriver):
        self._ssd = ssd
        self._loop_count = 100

    def execute(self) -> None:
        for lba in range(self._loop_count) :
            result = self._ssd.read(lba)
            print(f"[Read] LBA {lba:02d} : {result}")
