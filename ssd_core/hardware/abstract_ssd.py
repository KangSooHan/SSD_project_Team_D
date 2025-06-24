from abc import ABC, abstractmethod

class AbstractSSD(ABC):

    @abstractmethod
    def read(self, address: int) -> str:
        pass

    @abstractmethod
    def write(self, address: int, data: int) -> None:
        pass

    @abstractmethod
    def erase(self, address: int, size: int) -> None:
        pass
