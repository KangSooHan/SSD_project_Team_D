from copy import deepcopy
from typing import List, Tuple

from validator import Packet
from ssd_core.abstract_buffer_optimizer import AbstractBufferOptimizer


class SimpleBufferOptimizer(AbstractBufferOptimizer):
    """
    Reduce the number of buffer commands by removing or merging redundant ones:
    1. Drop writes invalidated by later erases.
    2. Keep only the final write per address.
    3. Merge erase commands into minimal fixed-size chunks,
       grouping all erases before writes.
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
        c) Merge erase commands into efficient chunks, then emit all erases before writes.
        """
        commands = self._drop_redundant_writes(commands)
        commands = self._drop_duplicate_writes(commands)
        commands = self._merge_erase_commands(commands)
        return commands

    def _drop_redundant_writes(self, commands: List[Packet]) -> List[Packet]:
        erase_ranges: List[Tuple[int, int]] = []
        filtered_rev: List[Packet] = []

        for cmd in reversed(commands):
            if cmd.COMMAND == "E":
                start = cmd.ADDR
                size = cmd.VALUE
                erase_ranges.append((start, start + size - 1))
                filtered_rev.append(cmd)
            elif cmd.COMMAND == "W":
                if any(s <= cmd.ADDR <= e for s, e in erase_ranges):
                    continue
                filtered_rev.append(cmd)
            else:
                filtered_rev.append(cmd)

        return list(reversed(filtered_rev))

    def _drop_duplicate_writes(self, commands: List[Packet]) -> List[Packet]:
        seen = set()
        filtered_rev: List[Packet] = []

        for cmd in reversed(commands):
            if cmd.COMMAND == "W":
                if cmd.ADDR in seen:
                    continue
                seen.add(cmd.ADDR)
            filtered_rev.append(cmd)

        return list(reversed(filtered_rev))

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
                end = start + sorted_cmds[idx].VALUE - 1
            else:
                end = start
            idx += 1

            while idx < len(sorted_cmds) and sorted_cmds[idx].ADDR <= end + 1:
                pkt = sorted_cmds[idx]
                pkt_end = (
                    pkt.ADDR + pkt.VALUE - 1 if pkt.COMMAND == "E" else pkt.ADDR
                )
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
        originals = [
            c for c in commands if c.COMMAND == "E" and start <= c.ADDR <= end
        ]
        span = end - start + 1
        needed = (span + self.MAX_ERASE_SIZE - 1) // self.MAX_ERASE_SIZE

        if needed >= len(originals):
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

    def _merge_erase_commands(self, commands: List[Packet]) -> List[Packet]:
        """
        Combine erase commands into optimal chunks (allowing
        bridging across writes), then emit all erases first
        followed by writes (and any other commands).
        """
        # Merge intervals across both E and W to allow write-bridging
        relevant = [c for c in commands if c.COMMAND in ("E", "W")]
        intervals = self._merge_intervals(relevant)

        # Generate the optimal erase chunks
        optimized_erases: List[Packet] = []
        for start, end in intervals:
            optimized_erases.extend(self._generate_erase_chunks(start, end, commands))

        # Sort erases by address
        optimized_erases.sort(key=lambda p: p.ADDR)

        # Collect remaining commands
        writes = [c for c in commands if c.COMMAND == "W"]
        writes.sort(key=lambda p: p.ADDR)
        others = [c for c in commands if c.COMMAND not in ("E", "W")]

        # Final sequence: all erases first, then writes, then others
        return optimized_erases + writes + others
