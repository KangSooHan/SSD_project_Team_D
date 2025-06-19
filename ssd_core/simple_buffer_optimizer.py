from ssd_core.abstract_buffer_optimizer import AbstractBufferOptimizer
from validator import Packet


class SimpleBufferOptimizer(AbstractBufferOptimizer):
    def calculate(self, buffer_lst: list[Packet]) -> list[Packet]:
        return buffer_lst