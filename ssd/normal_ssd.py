import os
from abstract_ssd import AbstractSSD

DATA_FILE = "ssd_nand.txt"

class NormalSSD(AbstractSSD):
    def read(self, address):
        pass
# ssd_nand.txt에 데이터를 기록
# 잘못된 LBA 범위면 ssd_output.txt에 "ERROR"로 기록된다.
    def write(self, address, data):
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'w') as file:
                file.write(f'{address} : {data}\n')

        else:
            with open(DATA_FILE, 'a') as file:
                file.write(f'{address} : {data}\n')

