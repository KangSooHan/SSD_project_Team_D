from validator import Packet
from ssd_core.abstract_ssd import AbstractSSD

class Buffer:
    def __init__(self, ssd:AbstractSSD):
        self._ssd = ssd
        self._memory:list[Packet] = []

    def is_full(self):
        return len(self._memory) == 5

    def __iter__(self):
        # 각 Packet에서 튜플 (COMMAND, ADDR, VALUE)로 변환
        return ((pkt.COMMAND, pkt.ADDR, pkt.VALUE) for pkt in self._memory)

    def flush(self):
        for packet in self._memory:
            if packet.COMMAND == "E":
                self._ssd.erase(packet.ADDR, packet.VALUE)
            elif packet.COMMAND == "W":
                self._ssd.write(packet.ADDR, packet.VALUE)
        self._memory = []

    def insert(self, packet:Packet):
        if packet.COMMAND in ["W", "E"]:
            if self.is_full():
                self.flush()
            else:
                self._memory.append(packet)
                self.optimize()

        if packet.COMMAND == "R":
            if self.is_value_in_buffer(packet.ADDR):
                pass
            else:
                self._ssd.read()

        if packet.COMMAND == "F":
            self.flush()

    def optimize(self):
        pass

    def fast_read_from(self, ADDR:int):
        return 1

    def is_value_in_buffer(self, ADDR:int):
        pass

    def __len__(self):
        return len(self._memory)