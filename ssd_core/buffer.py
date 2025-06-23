from ssd_core.buffer_optimizer_provider import BufferOptimizerProvider
from utils import to_4byte_hex_str
from validator import Packet
from ssd_core.normal_ssd import NormalSSD
import os


class Buffer:
    def __init__(self, ssd: NormalSSD):
        self._ssd = ssd
        self._memory: list[Packet] = []
        self.MAX_MEMORY_BUFFER = 5
        self.EMPTY_VALUE: str = "0x00000000"

        self._buffer_path = "buffer"
        os.makedirs(self._buffer_path, exist_ok=True)
        self.load_memory_from_files()

    def is_full(self):
        return len(self._memory) == self.MAX_MEMORY_BUFFER

    def flush(self):
        for packet in self._memory:
            if packet.COMMAND == "E":
                self._ssd.erase(packet.ADDR, packet.VALUE)
            elif packet.COMMAND == "W":
                self._ssd.write(packet.ADDR, packet.VALUE)
        self._memory = []
        self.save_memory_to_files()

    def insert(self, packet: Packet):
        if packet.COMMAND in ["W", "E"]:
            if self.is_full():
                self.flush()

            self._memory.append(packet)
            self.optimize()

            self.save_memory_to_files()
            return True

        if packet.COMMAND == "R":
            for mem in reversed(self._memory):
                if mem.COMMAND == "W":
                    if mem.ADDR != packet.ADDR:
                        continue

                    self._ssd._write_output(to_4byte_hex_str(mem.VALUE))
                    return True

                if mem.COMMAND == "E":
                    if not (mem.ADDR <= packet.ADDR < mem.ADDR + mem.VALUE):
                        continue

                    self._ssd._write_output(self.EMPTY_VALUE)
                    return True
            self._ssd.read(packet.ADDR)
            return True

        if packet.COMMAND == "F":
            self.flush()
            return True

        return False

    def clear(self):
        self._memory = []
        self.save_memory_to_files()

    def write_invalid_output(self):
        self._ssd._write_output(self._ssd.INVALID_OUTPUT)

    def optimize(self):
        optimize_strategy = BufferOptimizerProvider.get_instance(self._memory)
        self._memory = optimize_strategy.calculate(self._memory)

    def __len__(self):
        return len(self._memory)

    def load_memory_from_files(self):
        self._memory = []

        for i in range(1, self.MAX_MEMORY_BUFFER + 1):
            found = False
            for filename in os.listdir(self._buffer_path):
                if filename.startswith(f"{i}_") and filename.endswith(".txt"):
                    parts = filename[:-4].split("_")  # remove .txt
                    if len(parts) == 4:
                        _, cmd_str, addr_str, value_str = parts
                        command = cmd_str[0].upper()
                        addr = int(addr_str, 0)  # supports hex (0x), octal (0o), etc.

                        value = int(value_str, 0) if command == "write" else int(value_str, 16)
                        self._memory.append(Packet(COMMAND=command, ADDR=addr, VALUE=value))
                        found = True
                        break
            if not found:
                # empty file or no match
                continue

    def save_memory_to_files(self):
        exist_files = os.listdir(self._buffer_path)
        for file in exist_files:
            file_path = os.path.join(self._buffer_path, file)
            try:
                os.remove(file_path)
            except FileNotFoundError:
                pass

        for i in range(self.MAX_MEMORY_BUFFER):
            if i < len(self._memory):
                value = str(self._memory[i].VALUE) if self._memory[i].COMMAND.lower() == "write" else to_4byte_hex_str(self._memory[i].VALUE)
                filename = f"{i + 1}_{self._memory[i].COMMAND.lower()}_{self._memory[i].ADDR}_{value}.txt"
            else:
                filename = f"{i + 1}_empty.txt"

            filepath = os.path.join(self._buffer_path, filename)
            # Create the current file
            with open(filepath, "w") as f:
                f.write("")  # Empty content; can include metadata if needed
