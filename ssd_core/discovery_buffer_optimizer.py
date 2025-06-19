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