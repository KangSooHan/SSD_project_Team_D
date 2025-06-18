from ssd_core.abstract_ssd import AbstractSSD


class FullReadCommand:
    def __init__(self, ssd: AbstractSSD):
        self._ssd = ssd

    def execute(self) -> None:
        for lba in range(0, 100) :
            self._ssd.read(lba)
