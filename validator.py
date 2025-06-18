import re
from abc import ABC, abstractmethod
class Validator(ABC):
    def _is_valid_LBA(self, LBA:int) -> bool:
        try:
            return 0 <= int(LBA) < 100
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
            return 0x00000000 <= num <= 0xFFFFFFFF
        except ValueError:
            return False

    def _preprocess_sentence(self, sentence:str) -> str:
        sentence = sentence.strip()
        sentence = sentence.lower()
        return sentence

    def _validate_test(self, sentence:str):
        return self.run(sentence)[0] != False

    def run(self, sentence: str) -> (bool, int, int):
        try:
            sentence = self._preprocess_sentence(sentence)
            split_sentence = sentence.split(" ")
            return self._validate(split_sentence)
        except:
            return False, None, None

class SSDValidator(Validator):
    def _validate(self, split_sentence:list) -> (str, int, int):
        if not split_sentence:
            return False
        command = split_sentence[0]
        if command == "w":
            if len(split_sentence) != 3:
                return False, None, None
            addr, hex_value = split_sentence[1], split_sentence[2]
            if self._is_valid_LBA(addr) and self._is_valid_hex_value(hex_value):
                return "W", int(addr), int(hex_value, 16)

        if command == "r":
            if len(split_sentence) != 2:
                return False, None, None
            addr = split_sentence[1]
            if self._is_valid_LBA(addr):
                return "R", int(addr), None
        return False, None, None


class ShellValidator(Validator):
    def _validate(self, split_sentence: list) -> (str, int, int):
        if not split_sentence:
            return False

        command = split_sentence[0]
        if command == "write":
            if len(split_sentence) != 3:
                return False, None, None

            addr, hex_value = split_sentence[1], split_sentence[2]

            if self._is_valid_LBA(addr) and self._is_valid_hex_value(hex_value):
                return "write", int(addr), int(hex_value, 16)

        if command == "read":
            if len(split_sentence) != 2:
                return False, None, None
            addr = split_sentence[1]
            if self._is_valid_LBA(addr):
                return "read", int(addr), None

        if command == "help":
            if len(split_sentence) != 1:
                return False, None, None
            return "help", None, None

        if command == "exit":
            if len(split_sentence) != 1:
                return False, None, None
            return "exit", None, None

        if command == "fullwrite":
            if len(split_sentence) != 2:
                return False, None, None
            hex_value = split_sentence[1]
            if self._is_valid_hex_value(hex_value):
                return "fullwrite", None, int(hex_value, 16)

        if command == "fullread":
            if len(split_sentence) != 1:
                return False, None, None
            return "fullread", None, None

        return False, None, None