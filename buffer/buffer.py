class Buffer:
    def __init__(self):
        self.memory = []
    def insert(self, value:str):
        self.memory.append(value)

    def len(self):
        return len(self.memory)