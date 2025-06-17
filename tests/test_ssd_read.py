import os
import pytest
from ssd.normal_ssd import NormalSSD

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


def read_output() -> str:
    with open(OUTPUT_FILE, "r") as f:
        return f.read().strip()


@pytest.mark.parametrize("initial_nand, read_lba, expected_output", [
    # Valid reads - matching written LBA
    ({"0": "0x12345678"}, 0, "0x12345678"),
    ({"50": "0xABCDEF01"}, 50, "0xABCDEF01"),
    ({"99": "0xFFFFFFFF"}, 99, "0xFFFFFFFF"),

    # Valid LBA but not written
    ({"10": "0x11111111", "20": "0x22222222"}, 30, "0x00000000"),
    ({"10": "0x11111111"}, 11, "0x00000000"),
    ({}, 5, "0x00000000"),

    # Empty NAND
    ({}, 0, "0x00000000"),
    ({}, 99, "0x00000000"),

    # Edge of range with unrelated content
    ({"1": "0xAAAA0000", "98": "0xBBBB1111"}, 0, "0x00000000"),
    ({"1": "0xAAAA0000", "98": "0xBBBB1111"}, 99, "0x00000000"),

    # Invalid LBA range - below
    ({"3": "0xAAAABBBB"}, -1, "ERROR"),
    ({"0": "0x00000001"}, -10, "ERROR"),

    # Invalid LBA range - above
    ({"3": "0xAAAABBBB"}, 100, "ERROR"),
    ({"99": "0xDEADBEEF"}, 101, "ERROR"),
])
def test_read(initial_nand, read_lba, expected_output):
    if initial_nand:
        with open(NAND_FILE, "w") as f:
            for lba, value in initial_nand.items():
                f.write(f"{lba} {value}\n")

    ssd = NormalSSD()
    ssd.read(read_lba)

    assert read_output() == expected_output
