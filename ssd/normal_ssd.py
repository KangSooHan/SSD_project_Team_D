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
        if not os.path.exists(self._nand_file):
            open(self._nand_file, "w").close()

    def read(self, address: int) -> None:
        if address not in self._valid_lba_range:
            #self._file_write(self._output_file,'w',self.INVALID_OUTPUT)
            return

        with open(self._nand_file, "r") as f:
            for line in f:
                lba_str, value = line.strip().split()
                if int(lba_str) == address:
                    #self._file_write(self._output_file, 'w', '0x' + value)
                    self._write_output('0x' + value)
                    return

        #self._file_write(self._output_file, 'w',self.EMPTY_VALUE)
        self._write_output(self.EMPTY_VALUE)

    def _file_write(self, file_name, mode, value):
        with open(file_name, mode) as f:
            f.write(value)

    def _write_output(self, value: str) -> None:
        with open(self._output_file, "w") as f:
            f.write(value)

    def write(self, address: int, data: int) -> None:
        overwrite_flag = False
        if address not in self._valid_lba_range:
            #self._file_write(self._output_file,'w',self.INVALID_OUTPUT)
            self._write_output(self.INVALID_OUTPUT)
            return

        with open(self.DEFAULT_NAND_FILE, 'r+') as file:
            lines = file.readlines()
        with open(self.DEFAULT_NAND_FILE, 'r+') as file:
            if not lines:
                file.write(f'{address} 0x{data:08X}\n')
                return
            file.seek(0)
            file.truncate()

            for line in lines:
                written_lba, written_data = line.strip().split()
                new_line = line
                if int(written_lba) == address and not self._overwrite_flag:
                    overwrite_flag = True
                    new_data = f'0x{data:08X}'  # 16진수로 포맷
                    new_line = f'{written_lba} {new_data}\n'
                file.write(new_line)
            if not overwrite_flag:
                file.write(f'{address} 0x{data:08X}\n')
                #self._file_write(self.DEFAULT_NAND_FILE,"r+",f'{address} 0x{data:08X}\n')

ssd= NormalSSD()

ssd.write(20, 0xABABAABA)