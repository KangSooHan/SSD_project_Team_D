from ssd.abstract_ssd import AbstractSSD


class TestScenario1:
    RESULT_FAIL = "FAIL"
    RESULT_PASS = "PASS"

    def __init__(self, ssd: AbstractSSD):
        self._ssd = ssd

    def _to_4byte_hex_str(self, value: int):
        hex_str = f'0x{value:08X}'  # 대문자 출력
        return hex_str

    def execute(self):
        # test scenario from lecture note page #28
        for i in range(0, 100, 5):
            self._ssd.write(i, self._to_4byte_hex_str(i))
            self._ssd.write(i + 1, self._to_4byte_hex_str(i + 1))
            self._ssd.write(i + 2, self._to_4byte_hex_str(i + 2))
            self._ssd.write(i + 3, self._to_4byte_hex_str(i + 3))
            self._ssd.write(i + 4, self._to_4byte_hex_str(i + 4))

            if not self.read_compare(i, self._to_4byte_hex_str(i)): return TestScenario1.RESULT_FAIL
            if not self.read_compare(i + 1, self._to_4byte_hex_str(i + 1)): return TestScenario1.RESULT_FAIL
            if not self.read_compare(i + 2, self._to_4byte_hex_str(i + 2)): return TestScenario1.RESULT_FAIL
            if not self.read_compare(i + 3, self._to_4byte_hex_str(i + 3)): return TestScenario1.RESULT_FAIL
            if not self.read_compare(i + 4, self._to_4byte_hex_str(i + 4)): return TestScenario1.RESULT_FAIL

        return TestScenario1.RESULT_PASS

    def read_compare(self, address, data):
        result = self._ssd.read(address)

        return result == data
