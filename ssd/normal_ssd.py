import os
from ssd.abstract_ssd import AbstractSSD

class NormalSSD(AbstractSSD):
    DEFAULT_NAND_FILE: str = "ssd_nand.txt"
    DEFAULT_OUTPUT_FILE: str = "ssd_output.txt"
    INVALID_OUTPUT: str = "ERROR"
    EMPTY_VALUE: str = "0x00000000"
    DEFAULT_LBA_RANGE: range = range(0, 100)

    def __init__(
        self,
        nand_file: str = DEFAULT_NAND_FILE,
        output_file: str = DEFAULT_OUTPUT_FILE,
        lba_range: range = DEFAULT_LBA_RANGE,
    ) -> None:
        self.nand_file: str = nand_file
        self.output_file: str = output_file
        self.valid_lba_range: range = lba_range

        if not os.path.exists(self.nand_file):
            open(self.nand_file, "w").close()

    def read(self, address: int) -> None:
        if address not in self.valid_lba_range:
            self._write_output(self.INVALID_OUTPUT)
            return

        with open(self.nand_file, "r") as f:
            for line in f:
                lba_str, value = line.strip().split()
                if int(lba_str) == address:
                    self._write_output(value)
                    return

        self._write_output(self.EMPTY_VALUE)

    def write(self, address: int, value: int) -> None:
        pass

    def _write_output(self, value: str) -> None:
        with open(self.output_file, "w") as f:
            f.write(value)
