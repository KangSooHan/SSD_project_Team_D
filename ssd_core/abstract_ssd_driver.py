from abc import ABC, abstractmethod

class AbstractSSDDriver(ABC):
    @abstractmethod
    def write(self, address: int, data: str) -> None:
        pass

    @abstractmethod
    def read(self, address: int) -> str:
        pass
