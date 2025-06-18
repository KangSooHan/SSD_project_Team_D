import re
class Validator:
    def _is_valid_write_sentence_length(self, split_sentence:list) -> bool:
        if split_sentence[0] == 'w' and len(split_sentence) == 3:
            return True
        return False

    def _is_valid_read_sentence_length(self, split_sentence:list) -> bool:
        if split_sentence[0] == 'r' and len(split_sentence) == 2:
            return True
        return False

    def _is_valid_LBA(self, split_sentence:list) -> bool:
        try:
            LBA = split_sentence[1]
            LBA = int(LBA, 16)
            return 0 <= LBA < 100
        except ValueError:
            return False

    def _is_valid_hex_value(self, split_sentence: list) -> bool:
        if len(split_sentence) == 2:
            return True

        value = split_sentence[2]
        if not isinstance(value, str):
            return False

        # 0x로 시작하고 1~8자리 헥사 숫자(0~9, a~f, A~F)인지 확인
        pattern = r'^0x[0-9a-fA-F]{1,8}$'
        if not re.match(pattern, value):
            return False

        # 값 범위는 정규식이 이미 제한하긴 했지만 추가로 int 변환 후 검사해도 좋음
        try:
            num = int(value, 16)
            return 0x00000000 <= num <= 0xFFFFFFFF
        except ValueError:
            return False

    def _preprocess_sentence(self, sentence:str) -> str:
        sentence = sentence.strip()
        sentence = sentence.lower()
        return sentence

    def _is_valid_sentence_length(self, split_sentence) -> bool:
        if self._is_valid_write_sentence_length(split_sentence):
            return True
        if self._is_valid_read_sentence_length(split_sentence):
            return True
        return False

    def _validate(self, split_sentence:list) -> bool:
        try:
            if not self._is_valid_sentence_length(split_sentence):
                return False

            if not self._is_valid_LBA(split_sentence):
                return False

            if not self._is_valid_hex_value(split_sentence):
                return False

            return True
        except:
            return False

    def _validate_test(self, sentence:str):
        try:
            sentence = self._preprocess_sentence(sentence)
            split_sentence = sentence.split(" ")
            return self._validate(split_sentence)
        except:
            return False

    def run(self, sentence:str) -> (bool, int, int):
        try:
            sentence = self._preprocess_sentence(sentence)
            split_sentence = sentence.split(" ")
            if self._validate(split_sentence):
                if split_sentence[0] == "w":
                    return "W", int(split_sentence[1]), int(split_sentence[2], 16)
                if split_sentence[0] == "r":
                    return "R", int(split_sentence[1]), None
            return False, None, None
        except:
            return False, None, None