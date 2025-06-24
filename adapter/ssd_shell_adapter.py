import subprocess
from pathlib import Path

from adapter.ssd_adapter_interface import SSDShellInterface
from ssd_core.hardware.normal_ssd import NormalSSD


class SSDShellAdapter(SSDShellInterface):
    DEFAULT_SCRIPT = "ssd.py"
    DEFAULT_NAND_FILE = NormalSSD.DEFAULT_NAND_FILE
    DEFAULT_OUTPUT_FILE = NormalSSD.DEFAULT_OUTPUT_FILE

    def __init__(
            self,
            script: str = DEFAULT_SCRIPT,
            nand_file: str = DEFAULT_NAND_FILE,
            output_file: str = DEFAULT_OUTPUT_FILE,
    ) -> None:
        self._script = script
        self._nand_file = nand_file
        self._output_file = output_file

    def _run_cmd(self, *args: str) -> None:
        cmd = ["python", self._script, *args]
        subprocess.run(cmd, check=True)

    def read(self, addr: int) -> str:
        self._run_cmd("R", str(addr))
        return Path(self._output_file).read_text().strip()

    def write(self, addr: int, data: int) -> None:
        self._run_cmd("W", str(addr), f"0x{data:08X}")

    def erase(self, addr: int, size: int) -> None:
        self._run_cmd("E", str(addr), str(size))

    def flush(self) -> None:
        self._run_cmd("F")
