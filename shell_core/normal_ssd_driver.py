import subprocess
import time
from ssd_core.abstract_ssd_driver import AbstractSSDDriver
from ssd_core.normal_ssd import NormalSSD


class NormalSSDDriver(AbstractSSDDriver):
    DEFAULT_NAND_FILE: str = NormalSSD.DEFAULT_NAND_FILE
    DEFAULT_OUTPUT_FILE: str = NormalSSD.DEFAULT_OUTPUT_FILE

    def __init__(self,
                 ssd_script: str = "ssd.py",
                 nand_file: str = DEFAULT_NAND_FILE,
                 output_file: str = DEFAULT_OUTPUT_FILE):
        self.ssd_script = ssd_script
        self._nand_file: str = nand_file
        self._output_file: str = output_file

    def read(self, addr: int) -> str:
        # Run the read command
        subprocess.run(["python", self.ssd_script, "R", str(addr)], check=True)

        time.sleep(0.01)

        with open(self._output_file, "r") as f:
            result = f.read().strip()
        return result

    def write(self, addr: int, data: int) -> None:
        # Run the write command
        subprocess.run(["python", self.ssd_script, "W", str(addr), f"0x{data:08X}"], check=True)

    def erase(self, addr: int, size: int) -> None:
        # Run the erase command
        subprocess.run(["python", self.ssd_script, "E", str(addr), str(size)], check=True)
