import os
import pytest
from ssd_core.normal_ssd import NormalSSD


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
NAND_FILE: str = os.path.join(ROOT, "ssd_nand.txt")
OUTPUT_FILE: str = os.path.join(ROOT, "ssd_output.txt")

@pytest.fixture(autouse=True)
def clean_files():
    """Remove nand/output files before and after each test."""
    for f in [NAND_FILE, OUTPUT_FILE]:
        if os.path.exists(f):
            os.remove(f)
    yield
    for f in [NAND_FILE, OUTPUT_FILE]:
        if os.path.exists(f):
            os.remove(f)


def write_nand_file(data: dict[str, str]) -> None:
    with open(NAND_FILE, "w") as f:
        for lba, value in data.items():
            f.write(f"{lba} {value}\n")


def read_output() -> str:
    with open(OUTPUT_FILE, "r") as f:
        return f.read().strip()


@pytest.mark.parametrize("nand_contents, lba_to_read, expected_output", [
    # Valid reads - matching written LBA
    ({"0": "0x12345678"}, 0, "0x12345678"),
    ({"50": "0xABCDEF01"}, 50, "0xABCDEF01"),
    ({"99": "0xFFFFFFFF"}, 99, "0xFFFFFFFF"),

    # Valid LBA but not written
    ({"10": "0x11111111", "20": "0x22222222"}, 30, "0x00000000"),
    ({"10": "0x11111111"}, 11, "0x00000000"),

    # Empty NAND
    ({}, 0, "0x00000000"),
    ({}, 99, "0x00000000"),

    # Invalid LBA range
    ({"3": "0xAAAABBBB"}, -1, "ERROR"),
    ({"3": "0xAAAABBBB"}, 100, "ERROR"),
])
def test_read(nand_contents, lba_to_read, expected_output):
    write_nand_file(nand_contents)
    ssd = NormalSSD()

    ssd.read(lba_to_read)

    assert read_output() == expected_output


@pytest.mark.parametrize("initial_nand, write_lba, data", [
    # Clean NAND
    ({}, 0, "0x11111111"),
    ({}, 99, "0x22222222"),
    # Dirty NAND
    ({"0": "0x12345678"}, 50, "0x12345678"),
    ({"50": "0xABCDEF01"}, 25, "0xAAAAAAAA"),
    ({"99": "0xFFFFFFFF"}, 75, "0xABCDEFAB"),
    # Dirty NAND with Overwrite
    ({"0": "0x12345678"}, 0, "0x12341234"),
    ({"50": "0xABCDEF01"}, 50, "0xAAAAAAAA"),
    ({"99": "0xFFFFFFFF"}, 99, "0xABCDEFAB"),
])
def test_write(initial_nand, write_lba, data):
    if not os.path.exists(NAND_FILE):
        open(NAND_FILE, "w").close()
    if initial_nand:
        with open(NAND_FILE, "w") as f:
            for lba, value in initial_nand.items():
                f.write(f'{lba} {value}\n')
    ssd = NormalSSD()
    ssd.write(write_lba, int(data, 16))

    with open(NAND_FILE, 'r+') as file:
        lines = file.readlines()
        written_lba, written_data = lines[-1].strip().split()

    assert str(written_lba) == str(write_lba)
    assert written_data == data


@pytest.mark.parametrize("initial_nand, erase_lba, size", [
    # Clean NAND
    ({}, 0, 5), ({}, 99, 3), ({}, 50, 10),
])
def test_erase_NAND가_클린상태일때_빈상태이면_성공(initial_nand, erase_lba, size):
    if not os.path.exists(NAND_FILE):
        open(NAND_FILE, "w").close()
    if initial_nand:
        with open(NAND_FILE, "w") as f:
            for lba, value in initial_nand.items():
                f.write(f'{lba} {value}\n')
    ssd = NormalSSD()
    #act
    ssd.erase(erase_lba,size)
    #assert
    with open(NAND_FILE, "r") as f:
        content = f.read()
    assert content == ""
@pytest.mark.parametrize("initial_nand, erase_lba, size", [
    # Clean NAND
    ({"0": "0x12345678"}, 0, 1), ({"0": "0x12345678"}, 0, 5), ({"0": "0x12345678"}, 0, 10),
    ({"50": "0x12345678"}, 50, 1), ({"50": "0x12345678"}, 50, 5), ({"50": "0x12345678"}, 50, 10)
])
def test_erase_NAND가_더티상태일때_빈상태이면_성공(initial_nand, erase_lba, size):
    if not os.path.exists(NAND_FILE):
        open(NAND_FILE, "w").close()
    if initial_nand:
        with open(NAND_FILE, "w") as f:
            for lba, value in initial_nand.items():
                f.write(f'{lba} {value}\n')
    ssd = NormalSSD()
    #act
    ssd.erase(erase_lba, size)
    # assert: NAND_FILE 내용이 전부 0x00000000인지 확인
    with open(NAND_FILE, "r") as f:
        lines = f.readlines()

    # 모든 라인이 "0x00000000"인지 확인
    for line in lines:
        _, written_data = line.strip().split()
        assert written_data == "0x00000000"

@pytest.mark.parametrize("initial_nand, erase_lba, size", [
    ({"0": "0x12345678", "3": "0x12341234"}, 0, 5),
    ({"90": "0x12345678", "95": "0x12341234"}, 90, 10)
])
def test_erase_NAND가_두줄이상_더티상태일때_빈상태이면_성공(initial_nand, erase_lba, size):
    if not os.path.exists(NAND_FILE):
        open(NAND_FILE, "w").close()
    if initial_nand:
        with open(NAND_FILE, "w") as f:
            for lba, value in initial_nand.items():
                f.write(f'{lba} {value}\n')
    ssd = NormalSSD()
    # act
    ssd.erase(erase_lba, size)
    # assert: NAND_FILE 내용이 전부 0x00000000인지 확인
    with open(NAND_FILE, "r") as f:
        lines = f.readlines()

    # 모든 라인이 "0x00000000"인지 확인
    for line in lines:
        _, written_data = line.strip().split()
        assert written_data == "0x00000000"

@pytest.mark.parametrize("initial_nand, erase_lba, size", [
    ({"0": "0x12345678", "3": "0x12341234"}, 90, 5),
    ({"90": "0x12345678", "95": "0x12341234"}, 0, 10)
])
def test_erase_NAND가_두줄이상_더티상태일때_안지워지면_성공(initial_nand, erase_lba, size):
    if not os.path.exists(NAND_FILE):
        open(NAND_FILE, "w").close()
    if initial_nand:
        with open(NAND_FILE, "w") as f:
            for lba, value in initial_nand.items():
                f.write(f'{lba} {value}\n')
    ssd = NormalSSD()
    # act
    ssd.erase(erase_lba, size)

    #assert
    expected_erase_range = set(range(erase_lba, erase_lba + size))

    with open(NAND_FILE, "r") as f:
        lines = f.readlines()

    for line in lines:
        written_lba_str, written_data = line.strip().split()
        written_lba = int(written_lba_str)

        if written_lba in expected_erase_range:
            # 지운 영역은 반드시 0x00000000
            assert written_data == "0x00000000"
        else:
            # 지우지 않은 영역은 initial_nand 값과 동일해야 함
            expected_value = initial_nand.get(str(written_lba))
            # 파일에 있으면 초기값과 같아야 하고, 없으면 기본값(예: 0x00000000)일 수도 있음
            # 테스트 목적에 따라 처리
            assert written_data == expected_value