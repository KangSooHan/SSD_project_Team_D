class Buffer:
    def __init__(self):
        self.memory = []
    def insert(self, value:str):
        self.memory.append(value)
        if self.len() == 5:
            self.flush()

    def len(self):
        return len(self.memory)

    def flush(self):
        ret = self.memory.copy()
        self.memory = []
        return ret

    def _print(self):
        return self.memory