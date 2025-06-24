from adapter.ssd_adapter_interface import SSDShellInterface
from command_core.base_command import BaseCommand

class FullWriteCommand(BaseCommand):
    def __init__(self, ssd: AbstractSSDDriver, value: int):
        self._ssd = ssd
        self._loop_count = 100
        self._value = value

    def execute(self) -> None:
        for lba in range(self._loop_count):
            self._ssd.write(lba, self._value)