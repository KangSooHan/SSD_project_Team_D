import copy
from itertools import product
from ssd_core.abstract_buffer_optimizer import AbstractBufferOptimizer
from validator import Packet

VALUE_EMPTY = 0
VALUE_VALID = 1
VALUE_MARK = 2

class DiscoveryBufferOptimizer(AbstractBufferOptimizer):
    def calculate(self, buffer_lst: list[Packet]) -> list[Packet]:
        """
        plan
        - erase 영역을 모두 모은다
        - write 영역을 모두 모은다. erase가 덮어쓰는 경우는 제외 한다.
        - erase 이후에 write 되는 erase 영역을 mark 영역으로 정의하고 마킹한다.
        - mark 영역에 erase를 수행할지 말지를 0/1로 구분하여 경우의 수를 생성한다.
        - 경우의 수는 erase 1번 write 4번인 경우 2^4 = 16개가 생성된다.
        - 16개의 erase 경우에 수에 대해, 최소로 erase 하는 카운트 + write 카운트가 최적해가 된다. (라고 믿고 싶다)
        - erase를 최소로 하는 카운트는 greedy로 순차 선택하여도 최적해가 나온다. (고 밑고 있다)
        - 순회 하는 중,  current_count와 동률이 나올 경우 skip 후 다음 해를 시도 한다.
        """
        # project values
        erase_lst = self.project_erase(buffer_lst)
        write_lst = self.project_write(buffer_lst)
        check_lst = [i for i, val in enumerate(erase_lst) if val == VALUE_MARK]

        # iteration

        # find best

        # compare

        # return
        return buffer_lst


    def project_erase(self, buffer_lst: list[Packet]) -> list[int]:
        result = [0] * 100 # LBA 0~99
        for cmd in buffer_lst:
            if cmd.COMMAND == "E":
                for i in range(cmd.SIZE):
                    result[cmd.ADDR + i] = VALUE_VALID
        return result

    def project_write(self, buffer_lst) -> list[int]:
        result = [0] * 100  # LBA 0~99
        for cmd in buffer_lst:
            if cmd.COMMAND == "E":
                for i in range(cmd.SIZE):
                    result[cmd.ADDR + i] = VALUE_EMPTY # overwrite
            elif cmd.COMMAND == "W":
                result[cmd.ADDR] = VALUE_VALID # written
        return result