class Validator:
    def is_valid_write_sentence_length(self, split_sentence:list):
        if split_sentence[0] == 'w' and len(split_sentence) == 3:
            return True

    def is_valid_read_sentence_length(self, split_sentence:list):
        if split_sentence[0] == 'r' and len(split_sentence) == 2:
            return True

    def is_valid_LBA(self, LBA:str):
        try:
            LBA = int(LBA, 16)
            return 0 <= LBA < 100
        except ValueError:
            return False

    def is_valid_hex_value(value):
        try:
            if isinstance(value, str):
                # 16진수 문자열이면 정수로 변환 시도
                value_int = int(value, 16)
            else:
                value_int = int(value)

            return 0x00000000 <= value_int <= 0xFFFFFFFF
        except ValueError:
            return False

    def preprocess_sentence(self, sentence:str):
        sentence = sentence.strip()
        sentence = sentence.lower()
        return sentence

    def is_invalid_sentence_length(self, split_sentence):
        if self.is_valid_write_sentence_length(split_sentence):
            return True
        if self.is_valid_read_sentence_length(split_sentence):
            return True
        return False

    def run(self, sentence:str):
        try:
            sentence = self.preprocess_sentence(sentence)
            split_sentence = sentence.split(" ")

            if self.is_invalid_sentence_length(split_sentence):
                return False

            if not self.is_valid_LBA(split_sentence[1]):
                return False

            if not self.is_valid_hex_value(split_sentence[2]):
                return False

        finally:
            return False