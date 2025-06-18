from ssd.abstract_ssd import AbstractSSD


class TestScenario1:
    def __init__(self, ssd: AbstractSSD):
        self._ssd = ssd

    def execute(self):
        # data 자료형을 어떻게 사용할 것인지 논의 필요
        self._ssd.write(0x00, hex(0))
        self._ssd.write(0x01, hex(1))
        self._ssd.write(0x02, hex(2))
        self._ssd.write(0x03, hex(3))

    def read_compare(self, address, data):
        result = self._ssd.read(address)

        return result == data
