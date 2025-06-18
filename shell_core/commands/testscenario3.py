import random

from ssd_core.abstract_ssd import AbstractSSD


class TestScenario3:
    RESULT_FAIL = "FAIL"
    RESULT_PASS = "PASS"

    def __init__(self, ssd: AbstractSSD):
        self._ssd = ssd

    def _to_4byte_hex_str(self, value: int):
        hex_str = f'0x{value:08X}'  # 대문자 출력
        return hex_str

    def execute(self):
        # test scenario from lecture note page #30
        LOOP_COUNT = 200
        for i in range(LOOP_COUNT):
            first_random_value = random.randint(1, 10)
            self._ssd.write(0, self._to_4byte_hex_str(first_random_value))

            second_random_value = random.randint(1, 10)
            self._ssd.write(99, self._to_4byte_hex_str(second_random_value))

            if not self.read_compare(0, self._to_4byte_hex_str(first_random_value)): return TestScenario3.RESULT_FAIL
            if not self.read_compare(99, self._to_4byte_hex_str(second_random_value)): return TestScenario3.RESULT_FAIL

        return TestScenario3.RESULT_PASS

    def read_compare(self, address, data):
        result = self._ssd.read(address)

        return result == data
