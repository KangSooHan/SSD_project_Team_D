import os
import pytest
from ssd_core.normal_ssd import NormalSSD

NAND_FILE = "ssd_nand.txt"
OUTPUT_FILE = "ssd_output.txt"


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
    ssd.write(write_lba, int(data,16))

    with open(NAND_FILE, 'r+') as file:
        lines = file.readlines()
        written_lba, written_data = lines[-1].strip().split()

    assert str(written_lba) == str(write_lba)
    assert written_data == data