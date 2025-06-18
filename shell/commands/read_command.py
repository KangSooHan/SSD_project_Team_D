from ssd.abstract_ssd import AbstractSSD


class ReadCommand:
    def __init__(self, ssd: AbstractSSD):
        self._ssd = ssd

    def execute(self, lba: int) -> None:
        if lba < 0 or lba > 99:
            raise Exception
        self._ssd.read(lba)
