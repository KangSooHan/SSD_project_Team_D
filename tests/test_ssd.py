import pytest
import os
import io
from unittest.mock import patch
from ssd import main as ssd_main
from validator import SSDValidator, Packet
from contextlib import redirect_stdout

@pytest.fixture
def capture_stdout():
    def _capture(func, *args, **kwargs):
        buf = io.StringIO()
        with redirect_stdout(buf):
            func(*args, **kwargs)
        return buf.getvalue().strip()
    return _capture

NAND_FILENAME = "ssd_nand.txt"
OUTPUT_FILENAME = "ssd_output.txt"


@pytest.fixture(autouse=True)
def clean_files():
    for filename in [NAND_FILENAME, OUTPUT_FILENAME]:
        if os.path.exists(filename):
            os.remove(filename)
    yield
    for filename in [NAND_FILENAME, OUTPUT_FILENAME]:
        if os.path.exists(filename):
            os.remove(filename)


def prepare_nand_file(nand_data: dict[str, str]) -> None:
    with open(NAND_FILENAME, "w") as f:
        for lba_str, value_str in nand_data.items():
            f.write(f"{lba_str} {value_str}\n")


def get_output_content() -> str:
    if not os.path.exists(OUTPUT_FILENAME):
        return ""
    with open(OUTPUT_FILENAME, "r") as f:
        return f.read().strip()


@pytest.mark.parametrize("nand_content, cli_args, expected", [
    ({"3": "0xCAFEBABE"}, ["R", "3"], "0xCAFEBABE"),
    ({}, ["R", "42"], "0x00000000"),
    ({}, ["R", "100"], "ERROR"),
])
def test_read_command(nand_content, cli_args, expected):
    prepare_nand_file(nand_content)
    ssd_main(cli_args)
    assert get_output_content() == expected


@pytest.mark.parametrize("cli_args", [
    ["W", "10", "0x11111111"],
    ["W", "0", "0xCAFEBABE"],
])
def test_write_command_with_mock(cli_args):
    with patch("ssd_core.normal_ssd.NormalSSD.write") as mock_write:
        mock_write.return_value = None
        ssd_main(cli_args)

        lba = int(cli_args[1])
        value = int(cli_args[2], 16)
        mock_write.assert_called_once_with(lba, value)
        assert get_output_content() == ""


@pytest.mark.parametrize("write_args, read_args", [
    (["W", "77", "0xFEEDBEEF"], ["R", "77"]),
    (["W", "0", "0x12345678"], ["R", "0"]),
])
def test_write_then_read_with_write_mock(write_args, read_args):
    with patch("ssd_core.normal_ssd.NormalSSD.write") as mock_write:
        mock_write.return_value = None
        ssd_main(write_args)

        lba = int(write_args[1])
        value = int(write_args[2], 16)
        mock_write.assert_called_once_with(lba, value)

    ssd_main(read_args)
    output = get_output_content()
    assert output in {"0x00000000", "ERROR"}

@pytest.mark.parametrize(("write_args", "return_value"), [
    (["W", "77", "0xFEEDBEEF"], Packet(True, 77, 0xFEEDBEEF)),
    (["W", "0", "0x12345678"], Packet(True, 0, 0x12345678)),
    (["R", "77"], Packet(True, 77, None)),
    (["R", "0"], Packet(True, 0, None)),
])
def test_SSD_검증기_Mock_추가_및_실행(write_args, return_value):
    with patch("ssd.SSDValidator") as MockValidator:
        mock_validator_instance = MockValidator.return_value
        mock_validator_instance.run.return_value = return_value

        ssd_main(write_args)

        mock_validator_instance.run.assert_called_once_with(" ".join(write_args))

'''
새로운 main 함수를 구현할 때 사용한 pytest문
'''
# @pytest.mark.parametrize("args", [
#     (["W", "77", "0xFEEDBEEF"]),
#     (["R", "77"]),
#     (["W", "0", "0x12345678"]),
#     (["R", "0"]),
# ])
# def test_ssd_and_validator_output_match(args, capture_stdout):
#     from ssd import validate_main
#     output_ssd = capture_stdout(ssd_main, args)
#     output_validator = capture_stdout(validate_main, args)
#
#     assert output_ssd == output_validator, f"\nSSD: {output_ssd}\nValidator: {output_validator}"