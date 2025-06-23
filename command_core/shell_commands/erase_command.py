from command_core.base_command import BaseCommand
from shell_core.abstract_ssd_driver import AbstractSSDDriver
from command_core.utils.erase_utils import erase_by_chunksize

class EraseCommand(BaseCommand):
    def __init__(self, ssd: AbstractSSDDriver, lba: int, size: int):
        self._ssd = ssd
        self._lba = lba
        self._size = size

    def execute(self) -> None:
        # 음수 size 처리
        start = self._lba
        count = self._size

        if count < 0:
            start = self._lba + count + 1
            count = -count

        erase_by_chunksize(self._ssd, count, start)

