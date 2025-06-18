class Validator:
    def is_valid_write_sentence_length(self, split_sentence:list):
        if split_sentence[0] == 'w' and len(split_sentence) == 3:
            return True
        return False

    def is_valid_read_sentence_length(self, split_sentence:list):
        if split_sentence[0] == 'r' and len(split_sentence) == 2:
            return True
        return False

    def is_valid_LBA(self, split_sentence:list):
        try:
            LBA = split_sentence[1]
            LBA = int(LBA, 16)
            return 0 <= LBA < 100
        except ValueError:
            return False

    def is_valid_hex_value(self, split_sentence:list):
        try:
            if(len(split_sentence) == 2):
                return True

            value = split_sentence[2]
            if isinstance(value, str):
                value = value.lower()
                if not value.startswith('0x'):

                    return False
                value = int(value, 16)
            else:
                return False
            return 0x00000000 <= value <= 0xFFFFFFFF
        except ValueError:
            return False

    def preprocess_sentence(self, sentence:str):
        sentence = sentence.strip()
        sentence = sentence.lower()
        return sentence

    def is_valid_sentence_length(self, split_sentence):
        if self.is_valid_write_sentence_length(split_sentence):
            return True
        if self.is_valid_read_sentence_length(split_sentence):
            return True
        return False

    def run(self, sentence:str):
        try:
            sentence = self.preprocess_sentence(sentence)
            split_sentence = sentence.split(" ")

            if not self.is_valid_sentence_length(split_sentence):
                return False

            print(self.is_valid_LBA(split_sentence))
            if not self.is_valid_LBA(split_sentence):
                return False

            if not self.is_valid_hex_value(split_sentence):
                return False

            return True
        except:
            return False