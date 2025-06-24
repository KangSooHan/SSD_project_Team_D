import os
from ssd_core.hardware.abstract_ssd import AbstractSSD


def find_project_root() -> str:
    current = os.path.abspath(os.path.dirname(__file__))
    while True:
        if os.path.isfile(os.path.join(current, "requirements.txt")):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            return current
        current = parent


class NormalSSD(AbstractSSD):
    ROOT = find_project_root()
    DEFAULT_NAND_FILE = os.path.join(ROOT, "ssd_nand.txt")
    DEFAULT_OUTPUT_FILE = os.path.join(ROOT, "ssd_output.txt")
    INVALID_OUTPUT = "ERROR"
    EMPTY_VALUE = "0x00000000"
    LBA_RANGE = range(0, 100)
    SIZE_RANGE = range(0, 11)

    def __init__(
            self,
            nand_file: str = DEFAULT_NAND_FILE,
            output_file: str = DEFAULT_OUTPUT_FILE
    ) -> None:
        self._nand_file = nand_file
        self._output_file = output_file
        self._ensure_nand_file_exists()

    def _ensure_nand_file_exists(self):
        if not os.path.exists(self._nand_file):
            open(self._nand_file, "w").close()

    def read(self, address: int) -> None:
        if not self._is_valid_lba(address):
            self._write_output(self.INVALID_OUTPUT)
            return
        value = self._get_value_from_nand(address)
        self._write_output(value)

    def write(self, address: int, data: int) -> None:
        if not self._is_valid_lba(address):
            self._write_output(self.INVALID_OUTPUT)
            return

        lines = self._read_nand_file()
        updated = False

        for idx, (lba, _) in enumerate(lines):
            if lba == address:
                lines[idx] = (address, f'0x{data:08X}')
                updated = True
                break

        if not updated:
            lines.append((address, f'0x{data:08X}'))

        self._write_nand_file(lines)

    def erase(self, address: int, size: int) -> None:
        if not self._is_valid_erase(address, size):
            self._write_output(self.INVALID_OUTPUT)
            return

        erase_range = set(range(address, address + size))
        lines = self._read_nand_file()

        for idx, (lba, _) in enumerate(lines):
            if lba in erase_range:
                lines[idx] = (lba, self.EMPTY_VALUE)

        self._write_nand_file(lines)

    def _is_valid_lba(self, address: int) -> bool:
        return address in self.LBA_RANGE

    def _is_valid_erase(self, address: int, size: int) -> bool:
        return (
                address in self.LBA_RANGE
                and size in self.SIZE_RANGE
                and (address + size - 1) <= max(self.LBA_RANGE)
        )

    def _get_value_from_nand(self, address: int) -> str:
        lines = self._read_nand_file()
        for lba, value in lines:
            if lba == address:
                return value
        return self.EMPTY_VALUE

    def _write_output(self, value: str) -> None:
        with open(self._output_file, "w") as file:
            file.write(value)

    def _read_nand_file(self) -> list[tuple[int, str]]:
        with open(self._nand_file, "r") as file:
            return [
                (int(lba_str), value)
                for line in file if line.strip()
                for lba_str, value in [line.strip().split()]
            ]

    def _write_nand_file(self, lines: list[tuple[int, str]]) -> None:
        with open(self._nand_file, 'w') as file:
            for lba, value in lines:
                file.write(f"{lba} {value}\n")
