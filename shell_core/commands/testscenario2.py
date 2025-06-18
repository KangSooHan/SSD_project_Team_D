from ssd_core.abstract_ssd import AbstractSSD


class TestScenario2:
    RESULT_FAIL = "FAIL"
    RESULT_PASS = "PASS"

    def __init__(self, ssd: AbstractSSD):
        self._ssd = ssd
        self.test_constant = self._to_4byte_hex_str(1)

    def _to_4byte_hex_str(self, value: int):
        hex_str = f'0x{value:08X}'  # 대문자 출력
        return hex_str

    def execute(self):
        # test scenario from lecture note page #29
        LOOP_COUNT = 30

        for i in range(LOOP_COUNT):
            self._ssd.write(4, self.test_constant)
            self._ssd.write(0, self.test_constant)
            self._ssd.write(3, self.test_constant)
            self._ssd.write(1, self.test_constant)
            self._ssd.write(2, self.test_constant)

            if not self.read_compare(4, self.test_constant):
                print(TestScenario2.RESULT_FAIL)
                return

            if not self.read_compare(0, self.test_constant):
                print(TestScenario2.RESULT_FAIL)
                return

            if not self.read_compare(3, self.test_constant):
                print(TestScenario2.RESULT_FAIL)
                return

            if not self.read_compare(1, self.test_constant):
                print(TestScenario2.RESULT_FAIL)
                return

            if not self.read_compare(2, self.test_constant):
                print(TestScenario2.RESULT_FAIL)
                return

        print(TestScenario2.RESULT_PASS)
        return

    def read_compare(self, address, data):
        result = self._ssd.read(address)

        return result == data
