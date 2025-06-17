# import os
# import pytest
# from ssd.normal_ssd import NormalSSD
#
# NAND_FILE = "ssd_nand.txt"
# OUTPUT_FILE = "ssd_output.txt"


# @pytest.fixture(autouse=True)
# def clean_files():
#     """Remove nand/output files before and after each test."""
#     for f in [NAND_FILE, OUTPUT_FILE]:
#         if os.path.exists(f):
#             os.remove(f)
#     yield
#     for f in [NAND_FILE, OUTPUT_FILE]:
#         if os.path.exists(f):
#             os.remove(f)

#
# @pytest.mark.parametrize("initial_nand, write_lba, data", [
#     # Clean NAND
#     ({}, 0, "0x11111111"),
#     ({}, 99, "0x22222222"),
#     # Dirty NAND
#     ({"0": "0x12345678"}, 50, "0x12345678"),
#     ({"50": "0xABCDEF01"}, 25, "0xAAAAAAAA"),
#     ({"99": "0xFFFFFFFF"}, 75, "0xABCDEFAB"),
#     # Dirty NAND with Overwrite
#     ({"0": "0x12345678"}, 0, "0x12341234"),
#     ({"50": "0xABCDEF01"}, 50, "0xAAAAAAAA"),
#     ({"99": "0xFFFFFFFF"}, 99, "0xABCDEFAB"),
# ])
def test_write():
    pass
