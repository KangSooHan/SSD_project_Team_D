from ssd_core.abstract_ssd import AbstractSSD


class FullWriteCommand:
    def __init__(self, ssd: AbstractSSD, value: str):
        self._ssd = ssd
        self._loop_count = 100
        self._value = value

    def execute(self) -> None:
        for lba in range(self._loop_count):
            self._ssd.write(lba, self._value)
            print([])