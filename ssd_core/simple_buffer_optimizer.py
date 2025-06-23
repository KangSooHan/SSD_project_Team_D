from copy import deepcopy
from typing import List, Tuple

from validator import Packet
from ssd_core.abstract_buffer_optimizer import AbstractBufferOptimizer


class SimpleBufferOptimizer(AbstractBufferOptimizer):
    """
    Reduce the number of buffer commands by removing or merging redundant ones:
    1. Drop writes invalidated by later erases.
    2. Keep only the final write per address.
    3. Merge erase commands into minimal fixed-size chunks.
    """
    MAX_ERASE_SIZE = 10

    def calculate(self, command_buffer: List[Packet]) -> List[Packet]:
        """
        Iteratively optimize the command buffer until it stops changing.
        """
        prev_buffer = None
        curr_buffer = deepcopy(command_buffer)

        while curr_buffer != prev_buffer:
            prev_buffer, curr_buffer = curr_buffer, self._optimize_once(curr_buffer)

        return curr_buffer

    def _optimize_once(self, commands: List[Packet]) -> List[Packet]:
        """
        Single optimization pass:
        a) Remove writes covered by subsequent erases.
        b) Drop duplicate writes, retaining only the last per address.
        c) Merge erase commands into efficient chunks.
        """
        commands = self._drop_redundant_writes(commands)
        commands = self._drop_duplicate_writes(commands)
        commands = self._merge_erase_commands(commands)
        return commands

    def _drop_redundant_writes(self, commands: List[Packet]) -> List[Packet]:
        """
        Remove write commands (W, addr, value) if a later erase covers that addr.
        """
        erase_ranges: List[Tuple[int, int]] = []
        filtered_rev: List[Packet] = []

        for cmd in reversed(commands):
            if cmd.COMMAND == "E":
                start_addr = cmd.ADDR
                size = cmd.VALUE  # third field is size for E
                end_addr = start_addr + size - 1
                erase_ranges.append((start_addr, end_addr))
                filtered_rev.append(cmd)
            elif cmd.COMMAND == "W":
                if any(start <= cmd.ADDR <= end for start, end in erase_ranges):
                    continue
                filtered_rev.append(cmd)
            else:
                filtered_rev.append(cmd)

        return list(reversed(filtered_rev))

    def _drop_duplicate_writes(self, commands: List[Packet]) -> List[Packet]:
        """
        Keep only the last write per address in the buffer.
        """
        seen: set[int] = set()
        filtered_rev: List[Packet] = []

        for cmd in reversed(commands):
            if cmd.COMMAND == "W":
                if cmd.ADDR in seen:
                    continue
                seen.add(cmd.ADDR)
            filtered_rev.append(cmd)

        return list(reversed(filtered_rev))

    def _merge_erase_commands(self, commands: List[Packet]) -> List[Packet]:
        """
        Combine erase commands into intervals and convert into optimal chunks.
        """
        # Determine address intervals from W/E commands
        relevant = [c for c in commands if c.COMMAND in ("E", "W")]
        intervals = self._merge_intervals(relevant)

        optimized_erases: List[Packet] = []
        for start, end in intervals:
            optimized_erases.extend(
                self._generate_erase_chunks(start, end, commands)
            )

        # Rebuild buffer, replacing old erases in order
        erase_iter = iter(sorted(optimized_erases, key=lambda p: p.ADDR))
        next_erase = next(erase_iter, None)
        result: List[Packet] = []

        for cmd in commands:
            if cmd.COMMAND == "E":
                if next_erase:
                    result.append(next_erase)
                    next_erase = next(erase_iter, None)
            else:
                result.append(cmd)

        return result

    def _merge_intervals(self, commands: List[Packet]) -> List[Tuple[int, int]]:
        """
        Merge overlapping or adjacent address ranges from E/W commands.
        """
        sorted_cmds = sorted(commands, key=lambda c: c.ADDR)
        merged: List[Tuple[int, int]] = []
        idx = 0

        while idx < len(sorted_cmds):
            start = sorted_cmds[idx].ADDR
            if sorted_cmds[idx].COMMAND == "E":
                length = sorted_cmds[idx].VALUE
                end = start + length - 1
            else:
                end = start
            idx += 1
            while idx < len(sorted_cmds) and sorted_cmds[idx].ADDR <= end + 1:
                pkt = sorted_cmds[idx]
                if pkt.COMMAND == "E":
                    pkt_end = pkt.ADDR + pkt.VALUE - 1
                else:
                    pkt_end = pkt.ADDR
                end = max(end, pkt_end)
                idx += 1
            merged.append((start, end))

        return merged

    def _generate_erase_chunks(
        self, start: int, end: int, commands: List[Packet]
    ) -> List[Packet]:
        """
        For a given address range, either keep original erase packets
        or generate fixed-size chunks (size <= MAX_ERASE_SIZE).
        """
        # Gather original erases in the range
        originals = [
            c for c in commands
            if c.COMMAND == "E" and start <= c.ADDR <= end
        ]
        orig_count = len(originals)

        span = end - start + 1
        needed = (span + self.MAX_ERASE_SIZE - 1) // self.MAX_ERASE_SIZE

        if needed >= orig_count:
            return originals

        chunks: List[Packet] = []
        pos = start
        remaining = span
        while remaining > 0:
            size = min(self.MAX_ERASE_SIZE, remaining)
            chunks.append(Packet("E", pos, size))
            pos += size
            remaining -= size

        return chunks