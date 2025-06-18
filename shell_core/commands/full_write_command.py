from ssd_core.abstract_ssd import AbstractSSD


class FullWriteCommand:
    def __init__(self, ssd: AbstractSSD):
        self._ssd = ssd
        self._loop_count = 100

    def execute(self, value: int) -> None:
        for lba in range(self._loop_count):
            self._ssd.write(lba, value)
