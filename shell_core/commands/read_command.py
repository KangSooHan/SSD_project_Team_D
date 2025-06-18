from ssd_core.abstract_ssd import AbstractSSD


class ReadCommand:
    def __init__(self, ssd: AbstractSSD):
        self._ssd = ssd

    def execute(self, lba: int) -> None:
        if lba < 0 or lba > 99:
            raise Exception
        result = self._ssd.read(lba)
        print(f"[Read] LBA {lba:02d} : {result}")
