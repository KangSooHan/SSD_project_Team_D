from ssd_core.abstract_ssd import AbstractSSD


class TestScenario1:
    RESULT_FAIL = "FAIL"
    RESULT_PASS = "PASS"

    def __init__(self, ssd: AbstractSSD):
        self._ssd = ssd

    def execute(self):
        # test scenario from lecture note page #28
        for i in range(0, 100, 5):
            for j in range(0, 5):
                self._ssd.write(i+j, i+j)

            for j in range(0, 5):
                if not self.read_compare(i+j, i+j):
                    print(TestScenario1.RESULT_FAIL)
                    return

        print(TestScenario1.RESULT_PASS)
        return

    def read_compare(self, address, data):
        result = int(self._ssd.read(address), 16)
        return result == data