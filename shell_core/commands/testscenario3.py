import random

from ssd_core.abstract_ssd import AbstractSSD


class TestScenario3:
    RESULT_FAIL = "FAIL"
    RESULT_PASS = "PASS"

    def __init__(self, ssd: AbstractSSD):
        self._ssd = ssd

    def execute(self):
        # test scenario from lecture note page #30
        LOOP_COUNT = 200
        for i in range(LOOP_COUNT):
            first_random_value = random.randint(1, 10)
            self._ssd.write(0, first_random_value)

            second_random_value = random.randint(1, 10)
            self._ssd.write(99, second_random_value)

            if not self.read_compare(0, first_random_value):
                print(TestScenario3.RESULT_FAIL)
                return

            if not self.read_compare(99, second_random_value):
                print(TestScenario3.RESULT_FAIL)
                return

        print(TestScenario3.RESULT_PASS)
        return

    def read_compare(self, address, data):
        result = int(self._ssd.read(address), 16)

        return result == data
