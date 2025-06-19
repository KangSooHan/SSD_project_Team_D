from ssd_core.abstract_ssd import AbstractSSD
from command_core.base_command import BaseCommand
import random

class TestScenario(BaseCommand):
    RESULT_FAIL = "FAIL"
    RESULT_PASS = "PASS"
    def __init__(self, ssd: AbstractSSD):
        self._ssd = ssd
        self._test_constant = 1
        self._zero_constant = 0x00000000

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
        _loop_count = 30

        for i in range(_loop_count):
            self._ssd.write(4, self._test_constant)
            self._ssd.write(0, self._test_constant)
            self._ssd.write(3, self._test_constant)
            self._ssd.write(1, self._test_constant)
            self._ssd.write(2, self._test_constant)

            if not self.read_compare(4, self._test_constant):
                print(TestScenario2.RESULT_FAIL)
                return

            if not self.read_compare(0, self._test_constant):
                print(TestScenario2.RESULT_FAIL)
                return

            if not self.read_compare(3, self._test_constant):
                print(TestScenario2.RESULT_FAIL)
                return

            if not self.read_compare(1, self._test_constant):
                print(TestScenario2.RESULT_FAIL)
                return

            if not self.read_compare(2, self._test_constant):
                print(TestScenario2.RESULT_FAIL)
                return

        print(TestScenario2.RESULT_PASS)
        return

class TestScenario3(TestScenario):
    def execute(self):
        # test scenario from lecture note page #30
        _loop_count = 200
        for i in range(_loop_count):
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

class TestScenario4(TestScenario):
    def execute(self):
        # test scenario from 3day.pdf #8
        _loop_count = 30
        _erase_size = 3

        # 0 ~ 2번 LBA 삭제
        self._ssd.erase(0, _erase_size)

        # 0 ~ 2 값이 0x00000000 인지 검사
        for i in range(3):
            if not self.read_compare(0, self._zero_constant):
                print(TestScenario4.RESULT_FAIL)
                return

        # 2 ~ 98 까지 3개씩 wirte/overwirte/erase/readcompare, (0,1,99)제외
        for _ in range(_loop_count):
            for i in range(2, 99, 3):
                self._ssd.write(i, self._test_constant)
                self._ssd.write(i, self._test_constant)
                self._ssd.erase(i, _erase_size)

                # i ~ i+2 값이 0x00000000 인지 검사
                for j in range(i, i+3):
                    if not self.read_compare(j, self._zero_constant):
                        print(TestScenario4.RESULT_FAIL)
                        return

        print(TestScenario4.RESULT_PASS)
        return