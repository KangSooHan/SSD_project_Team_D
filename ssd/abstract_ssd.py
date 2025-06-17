from abc import ABC, abstractmethod

class AbstractSSD(ABC):
    @abstractmethod
    def read(self, address: int) -> None:
        pass

    @abstractmethod
    def write(self, address: int, data: str) -> None:
        pass