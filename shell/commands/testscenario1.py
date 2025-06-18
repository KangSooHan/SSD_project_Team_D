from ssd.abstract_ssd import AbstractSSD


class TestScenario1:
    RESULT_FAIL = "FAIL"
    RESULT_PASS = "PASS"

    def __init__(self, ssd: AbstractSSD):
        self._ssd = ssd

    def execute(self):
        # data 자료형을 어떻게 사용할 것인지 논의 필요, 이후 리팩토링 진행 예정
        for i in range(100):
            self._ssd.write(i, hex(i))
            self._ssd.write(i + 1, hex(i + 1))
            self._ssd.write(i + 2, hex(i + 2))
            self._ssd.write(i + 3, hex(i + 3))
            self._ssd.write(i + 4, hex(i + 4))

            if not self.read_compare(i, hex(i)): return TestScenario1.RESULT_FAIL
            if not self.read_compare(i + 1, hex(i + 1)): return TestScenario1.RESULT_FAIL
            if not self.read_compare(i + 2, hex(i + 2)): return TestScenario1.RESULT_FAIL
            if not self.read_compare(i + 3, hex(i + 3)): return TestScenario1.RESULT_FAIL
            if not self.read_compare(i + 4, hex(i + 4)): return TestScenario1.RESULT_FAIL

        return TestScenario1.RESULT_PASS

    def read_compare(self, address, data):
        result = self._ssd.read(address)

        return result == data
