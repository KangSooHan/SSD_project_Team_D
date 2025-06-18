class Validator:
    def is_valid_write_sentence_length(self, split_sentence:list):
        if split_sentence[0] == 'w' and len(split_sentence) == 3:
            return True

    def is_valid_read_sentence_length(self, split_sentence:list):
        if split_sentence[0] == 'r' and len(split_sentence) == 2:
            return True

    def is_valid_LBA(self, LBA:str):
        if 0 <= int(LBA) < 100:
            return True
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

        finally:
            return False