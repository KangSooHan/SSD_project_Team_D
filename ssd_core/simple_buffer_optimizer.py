from copy import deepcopy
from validator import Packet
from ssd_core.abstract_buffer_optimizer import AbstractBufferOptimizer  # 같은 폴더 내에 있어야 함


class SimpleBufferOptimizer(AbstractBufferOptimizer):
    MAX_BUFFER_SIZE = 5

    def calculate(self, buffer_lst: list[Packet]) -> list[Packet]:
        if len(buffer_lst) > self.MAX_BUFFER_SIZE:
            raise ValueError(f"Buffer size exceeds maximum of {self.MAX_BUFFER_SIZE}.")

        prev_len = -1
        current = deepcopy(buffer_lst)

        while len(current) != prev_len:
            prev_len = len(current)
            current = self._ignore_duplicate_writes(current)
            current = self._ignore_before_erase(current)
            current = self._merge_erases(current)

        return current

    def _ignore_duplicate_writes(self, packets: list[Packet]) -> list[Packet]:
        seen = set()
        result = []
        for pkt in reversed(packets):
            if pkt.COMMAND == "W":
                if pkt.ADDR not in seen:
                    seen.add(pkt.ADDR)
                    result.append(pkt)
            else:
                result.append(pkt)
        return list(reversed(result))

    def _ignore_before_erase(self, packets: list[Packet]) -> list[Packet]:
        result = []
        erased_ranges = []

        for pkt in reversed(packets):
            if pkt.COMMAND == "E":
                start = pkt.ADDR
                end = start + pkt.SIZE - 1
                erased_ranges.append((start, end))
                result.append(pkt)
            elif pkt.COMMAND == "W":
                if any(start <= pkt.ADDR <= end for start, end in erased_ranges):
                    continue
                result.append(pkt)
            else:
                result.append(pkt)
        return list(reversed(result))

    def _merge_erases(self, packets: list[Packet]) -> list[Packet]:
        result = []
        i = 0
        while i < len(packets):
            pkt = packets[i]
            if pkt.COMMAND != "E":
                result.append(pkt)
                i += 1
                continue

            start = pkt.ADDR
            end = start + pkt.SIZE - 1
            j = i + 1
            while j < len(packets):
                next_pkt = packets[j]
                if next_pkt.COMMAND != "E":
                    break
                next_start = next_pkt.ADDR
                next_end = next_start + next_pkt.SIZE - 1

                if next_start <= end + 1:
                    end = max(end, next_end)
                    j += 1
                else:
                    break

            new_size = end - start + 1
            if new_size <= 10:
                result.append(Packet("E", ADDR=start, SIZE=new_size))
                i = j
            else:
                result.append(pkt)
                i += 1
        return result
