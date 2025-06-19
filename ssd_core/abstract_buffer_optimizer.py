from abc import ABC, abstractmethod

from validator import Packet


class AbstractBufferOptimizer(ABC):
    @abstractmethod
    def calculate(self, buffer_lst: list[Packet]) -> list[Packet]:
        ...