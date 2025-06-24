from adapter.ssd_adapter_interface import SSDShellInterface
from command_core.base_command import BaseCommand
from command_core.exceptions import InvalidLBAError

class WriteCommand(BaseCommand):
    def __init__(self, ssd: SSDShellInterface, lba: int, value: str):
        self._ssd = ssd
        self._lba = lba
        self._value = value

    def execute(self) -> None:
        if self._lba < 0 or self._lba > 99:
            raise InvalidLBAError(self._lba)
        self._ssd.write(self._lba, self._value)
        print('[Write] Done')