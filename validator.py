class Validator:
    def run(self, sentence:str):
        split_sentence = sentence.split(" ")

        if(len(split_sentence) == 3):
            return True

        return False