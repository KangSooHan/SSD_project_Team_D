import re
from abc import ABC, abstractmethod
from dataclasses import dataclass


MAX_LBA_ADDRESS = 100
MAX_ERASE_SIZE = 10
MAX_LBA_INT_VALUE = 0xFFFFFFFF
DUMMY_DATA = 0x00000000

@dataclass
class Packet:
    COMMAND: str
    OP1: int = None
    OP2: int = None


class Validator(ABC):
    def _is_valid_LBA(self, LBA: int) -> bool:
        try:
            return 0 <= int(LBA) < MAX_LBA_ADDRESS
        except ValueError:
            return False

    def _is_valid_size_value(self, size: int) -> bool:
        try:
            return isinstance(int(size), int)
        except ValueError:
            return False

    def _is_valid_hex_value(self, hex_vlaue: str) -> bool:
        if not isinstance(hex_vlaue, str):
            return False

        # 0x로 시작하고 1~8자리 헥사 숫자(0~9, a~f, A~F)인지 확인
        pattern = r'^0x[0-9a-fA-F]{1,8}$'
        if not re.match(pattern, hex_vlaue):
            return False

        # 값 범위는 정규식이 이미 제한하긴 했지만 추가로 int 변환 후 검사해도 좋음
        try:
            num = int(hex_vlaue, 16)
            return 0x00000000 <= num <= MAX_LBA_INT_VALUE
        except ValueError:
            return False

    def _preprocess_sentence(self, sentence: str) -> str:
        sentence = sentence.strip()
        sentence = sentence.lower()
        return sentence

    def _validate_test(self, sentence: str):
        return self.run(sentence).COMMAND != "ERR"

    def _is_valid_erase_range(self, size):
        try:
            size_int = int(size)
            return 0 <= size_int <= MAX_ERASE_SIZE
        except ValueError:
            return False

    def run(self, sentence: str) -> (bool, int, int):
        try:
            sentence = self._preprocess_sentence(sentence)
            split_sentence = sentence.split(" ")
            return self._validate(split_sentence)
        except:
            return Packet("ERR")


class SSDValidator(Validator):

    def _validate(self, split_sentence: list) -> (str, int, int):
        if not split_sentence:
            return Packet("ERR")
        command = split_sentence[0]
        if command == "w":
            if len(split_sentence) != 3:
                return Packet("ERR")
            addr, hex_value = split_sentence[1], split_sentence[2]
            if self._is_valid_LBA(addr) and self._is_valid_hex_value(hex_value):
                return Packet("W", int(addr), int(hex_value, 16))

        if command == "r":
            if len(split_sentence) != 2:
                return Packet("ERR")
            addr = split_sentence[1]
            if self._is_valid_LBA(addr):
                return Packet("R", int(addr))

        if command == "e":
            if len(split_sentence) != 3:
                return Packet("ERR")
            addr, size = split_sentence[1], split_sentence[2]
            if self._is_valid_LBA(addr) and self._is_valid_size_value(size) and self._is_valid_erase_range(size):
                return Packet("E", int(addr), int(size))

        if command == "f":
            if len(split_sentence) != 1:
                return Packet("ERR")
            return Packet("F")

        return Packet("ERR")


class ShellValidator(Validator):
    def _validate(self, split_sentence: list) -> (str, int, int):
        if not split_sentence:
            return Packet("ERR")

        command = split_sentence[0]
        if command == "write":
            if len(split_sentence) != 3:
                return Packet("ERR")

            addr, hex_value = split_sentence[1], split_sentence[2]

            if self._is_valid_LBA(addr) and self._is_valid_hex_value(hex_value):
                return Packet("write", int(addr), int(hex_value, 16))

        if command == "read":
            if len(split_sentence) != 2:
                return Packet("ERR")
            addr = split_sentence[1]
            if self._is_valid_LBA(addr):
                return Packet("read", int(addr))

        if command == "help":
            if len(split_sentence) != 1:
                return Packet("ERR")
            return Packet("help")

        if command == "exit":
            if len(split_sentence) != 1:
                return Packet("ERR")
            return Packet("exit")

        if command == "fullwrite":
            if len(split_sentence) != 2:
                return Packet("ERR")
            hex_value = split_sentence[1]
            if self._is_valid_hex_value(hex_value):
                return Packet("fullwrite", None, int(hex_value, 16))

        if command == "fullread":
            if len(split_sentence) != 1:
                return Packet("ERR")
            return Packet("fullread")

        if command == "flush":
            if len(split_sentence) != 1:
                return Packet("ERR")
            return Packet("flush")

        if command == "erase":
            if len(split_sentence) != 3:
                return Packet("ERR")

            addr, size = split_sentence[1], split_sentence[2]

            if self._is_valid_LBA(addr) and self._is_valid_size_value(size):
                return Packet("erase", int(addr), int(size))

        if command == "erase_range":
            if len(split_sentence) != 3:
                return Packet("ERR")

            start, end = split_sentence[1], split_sentence[2]

            if self._is_valid_LBA(start) and self._is_valid_LBA(end):
                return Packet("erase_range", int(start), int(end))

        if command == "1_" or command == "1_FullWriteAndReadCompare".lower():
            if len(split_sentence) != 1:
                return Packet("ERR")
            return Packet("1_")

        if command == "2_" or command == "2_PartialLBAWrite".lower():
            if len(split_sentence) != 1:
                return Packet("ERR")
            return Packet("2_")

        if command == "3_" or command == "3_WriteReadAging".lower():
            if len(split_sentence) != 1:
                return Packet("ERR")
            return Packet("3_")

        if command == "4_" or command == "4_EraseAndWriteAging".lower():
            if len(split_sentence) != 1:
                return Packet("ERR")
            return Packet("4_")

        if command == "shell_scripts.txt":
            if len(split_sentence) != 1:
                return Packet("ERR")
            return Packet("Runner")

        return Packet("ERR")
