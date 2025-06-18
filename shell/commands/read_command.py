from ssd.abstract_ssd import AbstractSSD

class ReadCommand:
    def __init__(self, ssd: AbstractSSD):
        self._ssd = ssd

