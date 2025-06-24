from abc import ABC, abstractmethod

class SSDShellInterface(ABC):
    @abstractmethod
    def write(self, address: int, data: int) -> None:
        pass

    @abstractmethod
    def read(self, address: int) -> str:
        pass

    @abstractmethod
    def erase(self, address: int, size: int) -> None:
        pass

    @abstractmethod
    def flush(self) -> None:
        pass