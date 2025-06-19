from ssd_core.abstract_ssd import AbstractSSD
from command_core.base_command import BaseCommand
import random

class TestScenario(BaseCommand):
    RESULT_FAIL = "FAIL"
    RESULT_PASS = "PASS"
    def __init__(self, ssd: AbstractSSD):
        self._ssd = ssd
        self.test_constant = 1

    def read_compare(self, address, data):
        try:
            result = int(self._ssd.read(address), 16)
            return result == data
        except:
            return False

class TestScenario1(TestScenario):
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

class TestScenario2(TestScenario):
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

class TestScenario3(TestScenario):
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