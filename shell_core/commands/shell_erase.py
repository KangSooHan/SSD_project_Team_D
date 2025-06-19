from shell_core.commands.base_command import BaseCommand
from ssd_core.abstract_ssd import AbstractSSD

class EraseCommand:
    def __init__(self, ssd: AbstractSSD, lba: int, size: int):
        self._ssd = ssd
        self._lba = lba
        self._size = size

    def execute(self) -> None:
        # 음수 size 처리
        if self._size < 0:
            start = self._lba + self._size + 1
            count = -self._size
        else:
            start = self._lba
            count = self._size

        if count == 0:
            print("[Erase] Skipped: size is 0")
            return

        while count > 0:
            chunk = min(10, count)
            chunk_start = start
            chunk_end = start + chunk - 1

            # 유효 범위만큼 잘라서 실행
            valid_start = max(0, chunk_start)
            valid_end = min(99, chunk_end)

            if valid_start <= valid_end:
                valid_size = valid_end - valid_start + 1
                self._ssd.erase(valid_start, valid_size)
                print(f"[Erase] LBA {valid_start:02d} ~ {valid_end:02d} erased.")

            # 다음 chunk로 이동
            start += chunk
            count -= chunk