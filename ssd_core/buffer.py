from validator import Packet
from ssd_core.normal_ssd import NormalSSD

class Buffer:
    def __init__(self, ssd:NormalSSD):
        self._ssd = ssd
        self._memory:list[Packet] = []

    def is_full(self):
        return len(self._memory) == 5

    def flush(self):
        for packet in self._memory:
            if packet.COMMAND == "E":
                self._ssd.erase(packet.ADDR, packet.VALUE)
            elif packet.COMMAND == "W":
                self._ssd.write(packet.ADDR, packet.VALUE)
        self._memory = []

    def insert(self, packet:Packet):
        if packet.COMMAND in ["W", "E"]:
            self._memory.append(packet)
            self.optimize()
            if self.is_full():
                self.flush()
            return True

        if packet.COMMAND == "R":
            if self.is_value_in_buffer(packet.ADDR):
                pass
            else:
                self._ssd.read(packet.ADDR)
            return True

        if packet.COMMAND == "F":
            self.flush()
            return True

        return False

    def write_invalid_output(self):
        self._ssd._write_output(self._ssd.INVALID_OUTPUT)

    def optimize(self):
        pass

    def fast_read_from(self, ADDR:int):
        return 1

    def is_value_in_buffer(self, ADDR:int):
        return False

    def __len__(self):
        return len(self._memory)