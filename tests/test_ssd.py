import pytest
import os
import io
from unittest.mock import patch
from ssd import main_test as ssd_main
from validator import SSDValidator, Packet
from contextlib import redirect_stdout
from pytest_mock import MockerFixture

@pytest.fixture
def capture_stdout():
    def _capture(func, *args, **kwargs):
        buf = io.StringIO()
        with redirect_stdout(buf):
            func(*args, **kwargs)
        return buf.getvalue().strip()
    return _capture

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
NAND_FILE: str = os.path.join(ROOT, "ssd_nand.txt")
OUTPUT_FILE: str = os.path.join(ROOT, "ssd_output.txt")


@pytest.fixture(autouse=True)
def clean_files():
    for filename in [NAND_FILE, OUTPUT_FILE]:
        if os.path.exists(filename):
            os.remove(filename)
    yield
    for filename in [NAND_FILE, OUTPUT_FILE]:
        if os.path.exists(filename):
            os.remove(filename)


def prepare_nand_file(nand_data: dict[str, str]) -> None:
    with open(NAND_FILE, "w") as f:
        for lba_str, value_str in nand_data.items():
            f.write(f"{lba_str} {value_str}\n")


def get_output_content() -> str:
    if not os.path.exists(OUTPUT_FILE):
        return ""
    with open(OUTPUT_FILE, "r") as f:
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


@pytest.mark.skip
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

@pytest.mark.skip
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

@pytest.mark.parametrize("cli_args, initial_nand, expected_output, expected_nand_after", [
    # 정상 지움: lba 0~2 지움, 모두 0x00000000으로
    (["E", "0", "3"],
     {"0": "0xAAAABBBB", "1": "0xCCCCDDDD", "2": "0xEEEEFFFF"},
     "",
     {"0": "0x00000000", "1": "0x00000000", "2": "0x00000000"}),

    # 일부 지움: 일부만 영향을 줌
    (["E", "1", "2"],
     {"0": "0xAAAABBBB", "1": "0x11111111", "2": "0x22222222"},
     "",
     {"0": "0xAAAABBBB", "1": "0x00000000", "2": "0x00000000"}),

    # 유효 범위 밖: lba 100은 무효
    (["E", "100", "1"],
     {},
     "ERROR",
     {}),
])
def test_erase_command(cli_args, initial_nand, expected_output, expected_nand_after):
    prepare_nand_file(initial_nand)
    ssd_main(cli_args)

    # 1. output 확인
    assert get_output_content() == expected_output

    # 2. NAND 파일 내용 확인
    if expected_nand_after:
        with open(NAND_FILE, "r") as f:
            actual_lines = f.read().strip().splitlines()
            print(actual_lines)
        expected_lines = [f"{lba} {value}" for lba, value in expected_nand_after.items()]
        assert sorted(actual_lines) == sorted(expected_lines)
    else:
        # NAND 파일이 비어 있어야 함
        assert os.stat(NAND_FILE).st_size == 0