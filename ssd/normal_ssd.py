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
        self._nand_file: str = nand_file
        self._output_file: str = output_file
        self._valid_lba_range: range = lba_range

        self._overwrite_flag = False

        if not os.path.exists(self._nand_file):
            open(self._nand_file, "w").close()

    def read(self, address: int) -> None:
        if address not in self._valid_lba_range:
            self._write_output(self.INVALID_OUTPUT)
            return
          
        value = self._load_value_from_nand(address)
        self._write_output(value)

    def _load_value_from_nand(self, address: int) -> str:
        with open(self._nand_file, "r") as f:
            for line in f:
                parts = line.strip().split()
                lba_str, value = parts
                if int(lba_str) == address:
                    return value
        return self.EMPTY_VALUE


    def _write_output(self, value: str) -> None:
        with open(self._output_file, "w") as f:
            f.write(value)

    def write(self, address: int, data: int) -> None:
        if address not in self._valid_lba_range:
            self._write_output(self.INVALID_OUTPUT)
            return

        with open(self.DEFAULT_NAND_FILE, 'r+') as file:
            lines = file.readlines()  # 전체 줄을 미리 읽고
            if not lines:
                file.write(f'{address} 0x{data:08X}\n')
                return
            file.seek(0)  # 파일 처음으로 이동
            file.truncate()  # 기존 파일 내용을 비움

            for line in lines:
                written_lba, written_data = line.strip().split()
                new_line = line
                if int(written_lba) == address and not self._overwrite_flag:
                    self._overwrite_flag = True
                    new_data = f'0x{data:08X}'  # 16진수로 포맷
                    new_line = f'{written_lba} {new_data}\n'
                file.write(new_line)
            if not self._overwrite_flag:
                file.write(f'{address} 0x{data:08X}\n')

