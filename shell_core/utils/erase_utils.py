from ssd_core.abstract_ssd import AbstractSSD

def erase_by_chunksize(_ssd: AbstractSSD, count, start):
    while count > 0:
        chunk = min(10, count)
        chunk_start = start
        chunk_end = start + chunk - 1

        # 유효 범위만큼 잘라서 실행
        valid_start = max(0, chunk_start)
        valid_end = min(99, chunk_end)

        if valid_start <= valid_end:
            valid_size = valid_end - valid_start + 1
            _ssd.erase(valid_start, valid_size)
            print(f"[Erase] LBA {valid_start:02d} ~ {valid_end:02d} erased.")

        # 다음 chunk로 이동
        start += chunk
        count -= chunk