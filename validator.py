class Validator:
    def valid_write_sentence(self, split_sentence:list):
        if split_sentence[0] == 'w' and len(split_sentence) == 3:
            return True

    def valid_read_sentence(self, split_sentence:list):
        if split_sentence[0] == 'r' and len(split_sentence) == 2:
            return True

    def preprocess_sentence(self, sentence:str):
        sentence = sentence.strip()
        return sentence

    def run(self, sentence:str):
        sentence = self.preprocess_sentence(sentence)
        split_sentence = sentence.split(" ")

        if self.valid_write_sentence(split_sentence):
            return True

        if self.valid_read_sentence(split_sentence):
            return True

        return False