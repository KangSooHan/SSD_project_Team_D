from adapter.ssd_adapter_interface import SSDShellInterface
from command_core.base_command import BaseCommand
from command_core.exceptions import InvalidLBAError

class ReadCommand(BaseCommand):
    def __init__(self, ssd: SSDShellInterface, lba: int):
        self._ssd = ssd
        self._lba = lba

    def execute(self) -> None:
        if self._lba < 0 or self._lba > 99:
            raise InvalidLBAError(self._lba)
        result = self._ssd.read(self._lba)
        print(f"[Read] LBA {self._lba:02d} : {result}")
