from command_core.base_command import BaseCommand
from adapter.ssd_adapter_interface import SSDShellInterface
from command_core.utils.erase_utils import erase_by_chunksize

class EraseRangeCommand(BaseCommand):
    def __init__(self, ssd: SSDShellInterface, start: int, end: int):
        self._ssd = ssd
        self._start = start
        self._end = end

    def execute(self) -> None:
        # 음수 size 처리
        if self._start > self._end:
            self._start, self._end = self._end, self._start

        start = self._start
        end = self._end
        count = end - start + 1

        erase_by_chunksize(self._ssd, count, start)