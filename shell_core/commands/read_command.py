from ssd_core.abstract_ssd import AbstractSSD


class ReadCommand:
    def __init__(self, ssd: AbstractSSD, lba: int):
        self._ssd = ssd
        self._lba = lba

    def execute(self) -> None:
        if self._lba < 0 or self._lba > 99:
            raise Exception
        result = self._ssd.read(self._lba)
        print(f"[Read] LBA {self._lba:02d} : {result}")
