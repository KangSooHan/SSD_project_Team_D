from abc import ABC, abstractmethod

class AbstractSSD(ABC):
    @abstractmethod
    def read(self, address: int) -> str:
        """

        :param address: 0~99 범위의 주소 값
        :return: ssd_output.txt 파일의 값을 읽어 str 값을 반환한다.
                 address 오류 인 경우에도 ssd_output.txt에 "ERROR" 값이 출력되므로
                 별도의 예외 처리 기능이 필요하지 않다.
        """
        pass

    @abstractmethod
    def write(self, address: int, data: str) -> None:
        pass