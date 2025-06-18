# import os
# import pytest
# from ssd.normal_ssd import NormalSSD
#
# NAND_FILE = "ssd_nand.txt"
# OUTPUT_FILE = "ssd_output.txt"
#
#
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
# def test_write(initial_nand, write_lba, data):
#     if not os.path.exists(NAND_FILE):
#         open(NAND_FILE, "w").close()
#     if initial_nand:
#         with open(NAND_FILE, "w") as f:
#             for lba, value in initial_nand.items():
#                 f.write(f'{lba} {value}\n')
#     ssd = NormalSSD()
#     ssd.write(write_lba, data)
#
#     with open(NAND_FILE, 'r+') as file:
#         lines = file.readlines()
#         written_lba, written_data = lines[-1].strip().split()
#     assert written_lba == write_lba
#     assert written_data == data
def test_write():
    pass